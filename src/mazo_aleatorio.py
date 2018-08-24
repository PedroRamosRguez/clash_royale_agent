import requests
import parsear_respuesta
import random
import simpleCard

#variable global para guardar el mazo aleatorio creado y no perderlo hasta que se genere otro distinto
mazo_aleatorio_creado = []

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
    #para usar https usar esta url: https://clashapi.now.sh/api/cards/
    url = 'http://www.clashapi.xyz/api/random-deck'
    respuesta = requests.get(url)
    datos = respuesta.json()
    mazo = [x['idName'] for x in datos]
    return datos


def get_mazo_espanol():
    """
        Función para obtener el mazo aleatorio llamando a la api creada.
    """
    url = 'http://localhost:50000/api/card/'
    respuesta = requests.get(url)
    datos = respuesta.json()
    cartas_seleccionadas = random.sample(range(0, len(datos)), 8)
    mazo_creado = [datos[i] for i in cartas_seleccionadas]
    return mazo_creado


def get_listado_cartas_2(mazo):
    """
        Función para crear la listSelect de dialogflow en la app y mostrar el mazo creado
    """
    listado_cartas, elixirCost, arena = [], [], []
    for i in mazo:
        elixirCost.append(i['elixirCost'])
        arena.append(i['arena'])
        listado_cartas.append({
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
    return {'listado_cartas':listado_cartas, 'elixirCost':elixirCost, 'arena':arena }


def get_carta_seleccionada(carta):
    """
        Funcion para obtener los detalles de la carta desde la api
    """
    url = 'http://localhost:50000/api/card/'+carta
    respuesta = requests.get(url)
    datos = respuesta.json()
    return datos


def set_card_selected(card_seleted):
    """
        Función para crear la card de dialogflow con la informacion detallada de la carta seleccionada del mazo aleatorio creado.
    """
    listado_sugerencias = get_sugerencias()
    mensaje_voz = '''<speak>{} <break time = '800ms'/>
    <prosody rate="default">
    ¿Qué información desea escuchar?
    <break time = '700ms'/>
    {}</prosody></speak>
    '''
    card_details = simpleCard.set_card_details(
        mensaje_voz,
        card_seleted,
        listado_sugerencias
    )
    return card_details


def detalle_card(req):
    """action ver carta en detalle
        Función que activa la action de ver la carta de detalle y devuelve la respuesta al usuario
    """
    card_selected = req['originalDetectIntentRequest']['payload']['inputs']
    contenido_carta = get_carta_seleccionada(card_selected[0]['arguments'][0]['textValue'])
    result = set_card_selected(contenido_carta)
    #detalles_carta = get_carta_seleccionada(carta_seleccionada[0]['arguments'][0]['textValue'])
    #print(detalles_carta)
    response = parsear_respuesta.parsear_respuesta(result)
    return response


def mazo_aleatorio(req = None):
    """action de mazo aleatorio
        Action que llama a la API para obtener un mazo aleatorio
    """
    #mazo = get_mazo_aleatorio()
    mazo = get_mazo_espanol()
    listado_cartas = get_listado_cartas_2(mazo)
    #igualo las listas para la action del detalle y no perder el mazo creado
    global mazo_aleatorio_creado
    mazo_aleatorio_creado = listado_cartas
    print('ESTO ES EL LISTADO DE CARTAS...')
    coste_elixir = [i for i in listado_cartas['elixirCost']]
    arenas = [i for i in listado_cartas['arena']]
    media_coste_elixir = round(sum(coste_elixir)/ len(coste_elixir))
    top_arena = max(arenas)
    mensaje_voz = ''.join('''<speak><emphasis level='strong'>
    este es el mazo resultante: <break time='500ms'/> <break time='500ms'/>''')
    for i in listado_cartas['listado_cartas']:
        mensaje_voz = mensaje_voz + '''{}<break time='500ms'/>'''.format(i['title'])
    mensaje_voz = mensaje_voz + '''.Tiene una media de coste de elixir de {}
    y es un mazo de arena {}</emphasis></speak>'''.format(media_coste_elixir, top_arena)
    result = {
        'fulfillmentText': 'este es el mazo resultante',
        'fulfillmentMessages': [
            {
                'platform': 'ACTIONS_ON_GOOGLE',
                'simpleResponses': {
                    'simpleResponses': [
                        {
                            'textToSpeech': mensaje_voz,#'{}. Tiene una media de coste de elixir de {} y es un mazo de arena {}'.format(mensaje_voz,media_coste_elixir, top_arena),
                            'displayText': 'Mazo resultante.\n Media de coste de elixir de {} .\n Mazo de arena {}'.format(media_coste_elixir, top_arena),
                        }
                    ]
                }
            },
            {
                'platform': 'ACTIONS_ON_GOOGLE',
                'listSelect': {
                    "title": "Mazo generado",
                    'items': [i for i in listado_cartas['listado_cartas']]
                },

            },
        ],
    }
    respuesta = parsear_respuesta.parsear_respuesta(result)
    return respuesta