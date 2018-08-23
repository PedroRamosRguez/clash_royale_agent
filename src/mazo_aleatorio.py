import requests
import parsear_respuesta
import random
from googletrans import Translator

def get_mazo_aleatorio():
    url = 'http://www.clashapi.xyz/api/random-deck'
    respuesta = requests.get(url)
    datos = respuesta.json()
    mazo = [x['idName'] for x in datos]
    return datos


def get_mazo_espanol():
    url = 'http://localhost:50000/api/card/'
    respuesta = requests.get(url)
    datos = respuesta.json()
    cartas_seleccionadas = random.sample(range(0,len(datos)), 8)
    mazo_creado = [datos[i] for i in cartas_seleccionadas]
    return mazo_creado


def get_listado_cartas_2(mazo):
    listado_cartas, elixirCost, arena = [], [], []
    translator = Translator()
    #la traduccion de la descripcion dejarla pendiente...
    for i in mazo:
        elixirCost.append(i['elixirCost'])
        arena.append(i['arena'])
        # descripcion = i['description'] if 'description' in i.keys() else ''
        # descripcion_traducida = translator.translate(descripcion,dest='es')
        # print(descripcion_traducida.text)
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
            'title': i['idName']
        })
    return {'listado_cartas':listado_cartas, 'elixirCost':elixirCost, 'arena':arena }



def mazo_aleatorio(req = None):
    """action de mazo aleatorio
        Action que llama a la API para obtener un mazo aleatorio
    """
    #mazo = get_mazo_aleatorio()
    mazo = get_mazo_espanol()
    listado_cartas = get_listado_cartas_2(mazo)
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
                # opcion 1 para mostrar los resultados del carousel cardº
                'platform': 'ACTIONS_ON_GOOGLE',
                # 'carouselSelect': {
                #     'items': [i for i in listado_cartas['listado_cartas']]
                # },
                #opcion 2 para mostrar los resultados como una lista...
                'listSelect': {
                    "title": "Mazo generado",
                    'items': [i for i in listado_cartas['listado_cartas']]
                },

            },
        ],
    }
    respuesta = parsear_respuesta.parsear_respuesta(result)
    return respuesta