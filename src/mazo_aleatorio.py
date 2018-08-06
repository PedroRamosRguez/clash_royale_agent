import requests
import parsear_respuesta
from googletrans import Translator

def get_mazo_aleatorio():
    url = 'http://www.clashapi.xyz/api/random-deck'
    respuesta = requests.get(url)
    datos = respuesta.json()
    return datos

#obtiene un listado de cartas del tipo carousel card.
def get_listado_cartas(mazo):
    """"
        Método para añadir al objeto del carousel de cards las cards obtenidas
        del mazo aleatorio generado por la API
    """
    listado_cartas, elixirCost, arena = [], [], []
    #la traduccion de la descripcion dejarla pendiente...
    for i in mazo:
        #descripcion = i['description']
        #descripcion_traducida = translator.translate(descripcion, dest='es')
        elixirCost.append(i['elixirCost'])
        arena.append(i['arena'])
        listado_cartas.append({
            'info': {
                'key': i['idName'],
                'synonyms': [
                    i['name'],
                ]
            },
            'title': i['name'],
            'description': '',#i['description'],#str(descripcion_traducida.text),
            'image': {
                'imageUri': 'http://www.clashapi.xyz/images/cards/'+str(i['idName'])+'.png',
                'accessibilityText': str(i['idName'])
            },
        })
    return {'listado_cartas':listado_cartas, 'elixirCost':elixirCost, 'arena':arena }


def get_listado_cartas_2(mazo):
    listado_cartas, elixirCost, arena = [], [], []
    #la traduccion de la descripcion dejarla pendiente...
    for i in mazo:
        #descripcion = i['description']
        #descripcion_traducida = translator.translate(descripcion, dest='es')
        elixirCost.append(i['elixirCost'])
        arena.append(i['arena'])
        listado_cartas.append({
            # 'info': {
            #     'key': i['idName'],
            #     'synonyms': [
            #         i['name'],
            #     ]
            # },
            # 'title': i['name'],
            # 'description': '',#i['description'],#str(descripcion_traducida.text),
            # 'image': {
            #     'imageUri': 'http://www.clashapi.xyz/images/cards/'+str(i['idName'])+'.png',
            #     'accessibilityText': str(i['idName'])
            # },
            'description':i['description'],
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
    mazo = get_mazo_aleatorio()
    listado_cartas = get_listado_cartas(mazo)
    #listado_cartas = get_listado_cartas_2(mazo)
    print(listado_cartas['listado_cartas'])
    print('ESTO ES EL LISTADO DE CARTAS...')
    coste_elixir = [i for i in listado_cartas['elixirCost']]
    arenas = [i for i in listado_cartas['arena']]
    media_coste_elixir = round(sum(coste_elixir)/ len(coste_elixir))
    top_arena = max(arenas)
    result = {
        'fulfillmentText': 'este es el mazo resultante',
        'fulfillmentMessages': [
            {
                'platform': 'ACTIONS_ON_GOOGLE',
                'simpleResponses': {
                    'simpleResponses': [
                        {
                            'textToSpeech': 'este es el mazo resultante tiene una media de coste de elixir de {} y es un mazo de arena {}'.format(media_coste_elixir, top_arena),
                            'displayText': 'Mazo resultante.\n Media de coste de elixir de {} .\n Mazo de arena {}'.format(media_coste_elixir, top_arena),
                        }
                    ]
                }
            },
            {
                # opcion 1 para mostrar los resultados del carousel card
                'platform': 'ACTIONS_ON_GOOGLE',
                'carouselSelect': {
                    'items': [i for i in listado_cartas['listado_cartas']]
                },
                #opcion 2 para mostrar los resultados como una lista...
                # 'listSelect': {
                #     "title": "Mazo generado",
                #     'items': [i for i in listado_cartas['listado_cartas']]
                # },

            },
        ],
    }
    respuesta = parsear_respuesta.parsear_respuesta(result)
    return respuesta