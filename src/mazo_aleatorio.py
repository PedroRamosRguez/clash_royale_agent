import requests
import parsear_respuesta
import random
import simpleCard, ver_mazo_aleatorio_creado, sugerencias

#variable global para guardar el mazo aleatorio creado y no perderlo hasta que se genere otro distinto
random_created_deck = []

def get_sugerencias():
    """
        función para obtener las sugerencias y añadirlas a los botones de sugerencias del asistemte
    """
    sugerencias = [
        {
            'title': 'Generar mazo aleatorio',
        },
        {
            'title': 'Volver a mazo creado',
        },
        {
            'title': 'Salir',
        },
    ]
    return sugerencias


def get_mazo_aleatorio():
    """
        Función que llama a la api para obtener el mazo aleatorio con la información en inglés.
        Esta función se usa cuando el agente es cargado en idioma inglés o en países con habla
        inglesa.
    """
    #para usar https usar esta url: https://clashapi.now.sh/api/cards/
    url = 'http://www.clashapi.xyz/api/random-deck'
    response = requests.get(url)
    data = response.json()
    return data


def get_random_spanish_deck():
    """
        Función para obtener el mazo aleatorio con la información en español llamando a la
        api creada.
    """
    url = 'http://localhost:50000/api/card/'
    response = requests.get(url)
    data = response.json()
    selected_cards = random.sample(range(0, len(data)), 8)
    deck_created = [data[i] for i in selected_cards]
    return deck_created


def get_card_list(deck):
    """
        Función para crear la listSelect de dialogflow en la app y mostrar el mazo creado
    """
    #listado_cartas, elixirCost, arena = [], [], []
    card_list, elixirCost, arena = [], [], []
    for i in deck:
        elixirCost.append(i['elixirCost'])
        arena.append(i['arena'])
        card_list.append({
            'description':i['description'] if 'description' in i.keys() else '',
            'image':{
                'imageUri': 'http://www.clashapi.xyz/images/cards/'+str(i['idName'])+'.png',
                'accessibilityText': str(i['idName'])
            },
            'info': {
                'key': i['idName'],
                'synonyms': [
                    i['name'],
                ]
            },
            'title': i['name']
        })
    return {'card_list':card_list, 'elixirCost':elixirCost, 'arena':arena }


def get_selected_card(card):
    """
        Funcion para obtener los detalles de la carta desde la api
    """
    url = 'http://localhost:50000/api/card/'+card
    response = requests.get(url)
    data = response.json()
    return data


def set_card_selected(card_selected):
    """
        Función para crear la card de dialogflow con la informacion detallada de la carta seleccionada del mazo aleatorio creado.
    """
    listado_sugerencias = get_sugerencias()
    speech_sugerencias = sugerencias.escuchar_sugerencias(listado_sugerencias)
    mensaje_voz = '''<speak><emphasis level='strong'>Esta es la información correspondiente a la carta {}<break time = '800ms'/>
    {}<break time = '600ms'/>
    Es una carta {}<break time = '600ms'/> y
    tiene un coste de elixir de {}<break time = '800ms'/>
    <prosody rate="default">
    ¿Qué información desea escuchar?
    <break time = '700ms'/>
    {}</prosody></emphasis></speak>
    '''.format(card_selected['name'], card_selected['description'], card_selected['rarity'], card_selected['elixirCost'], speech_sugerencias)
    mensaje_card = '''Esta es la información correspondiente a la carta {}
    {}.\n Es una carta {} y tiene un coste de elixir de {}
    '''.format(card_selected['name'], card_selected['description'], card_selected['rarity'], card_selected['elixirCost'])
    card_details = simpleCard.set_card_details(
        mensaje_voz,
        mensaje_card,
        card_selected,
        listado_sugerencias
    )
    return card_details


def card_detail(req):
    """action ver carta en detalle
        Función que activa la action de ver la carta de detalle y devuelve la respuesta al usuario
    """
    card_selected = req['originalDetectIntentRequest']['payload']['inputs']
    card_details = get_selected_card(card_selected[0]['arguments'][0]['textValue'])
    result = set_card_selected(card_details)
    response = parsear_respuesta.parsear_respuesta(result)
    return response


def random_deck(req=None):
    """action de mazo aleatorio
        Action que llama a la API para obtener un mazo aleatorio
    """
    deck = get_random_spanish_deck()
    card_list = get_card_list(deck)
    #igualo las listas para la action del detalle y no perder el mazo creado
    global random_created_deck
    random_created_deck = card_list
    elixir_cost = [i for i in card_list['elixirCost']]
    arenas = [i for i in card_list['arena']]
    average_elixir_cost = round(sum(elixir_cost)/ len(elixir_cost))
    top_arena = max(arenas)
    voice_message = ''.join('''<speak><emphasis level='strong'>
    este es el mazo resultante: <break time='500ms'/> <break time='500ms'/>''')
    for i in card_list['card_list']:
        voice_message = voice_message + '''{}. <break time='800ms'/>'''.format(i['title'])
    voice_message = voice_message + '''.Tiene un coste medio de elixir de {}
    y es un mazo de arena {}</emphasis></speak>'''.format(average_elixir_cost, top_arena)
    result = {
        'fulfillmentText': 'este es el mazo resultante',
        'fulfillmentMessages': [
            {
                'platform': 'ACTIONS_ON_GOOGLE',
                'simpleResponses': {
                    'simpleResponses': [
                        {
                            'textToSpeech': voice_message,
                            'displayText': 'Mazo resultante.\n Media de coste de elixir de {} .\n Mazo de arena {}'.format(average_elixir_cost, top_arena),
                        }
                    ]
                }
            },
            {
                'platform': 'ACTIONS_ON_GOOGLE',
                'listSelect': {
                    "title": "Mazo generado",
                    'items': [i for i in card_list['card_list']]
                },

            },
        ],
    }
    response = parsear_respuesta.parsear_respuesta(result)
    return response


def deck_created(req=None):
    """action ver_mazo_creado
        Action que permite ver el mazo creado por la api. Se controla la respuesta en caso de que se haya creado o no.
    """
    if random_created_deck:
        result = ver_mazo_aleatorio_creado.show_created_deck(random_created_deck)
    else:
        result = {
            'fulfillmentMessages': [
                {
                    'platform': 'ACTIONS_ON_GOOGLE',
                    'simpleResponses': {
                        'simpleResponses': [
                            {
                                'textToSpeech': 'No se ha creado ningún mazo aleatorio',
                                'displayText': 'No se ha creado ningún mazo aleatorio',
                            }
                        ]
                    }
                },
                {
                    'platform': 'ACTIONS_ON_GOOGLE',
                    'suggestions': {
                        'suggestions': get_sugerencias(),
                    }
                }, 
            ]
        }
    response = parsear_respuesta.parsear_respuesta(result)
    return response