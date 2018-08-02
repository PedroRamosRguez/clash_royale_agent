import requests
import parsear_respuesta
from googletrans import Translator

def get_mazo_aleatorio():
    url = 'http://www.clashapi.xyz/api/random-deck'
    respuesta = requests.get(url)
    datos = respuesta.json()
    return datos

def get_listado_cartas(mazo):
    """"
        Método para añadir al objeto del carousel de cards las cards obtenidas
        del mazo aleatorio generado por la API
    """
    listado_cartas = []
    #la traduccion de la descripcion dejarla pendiente...
    for i in mazo:
        #descripcion = i['description']
        #descripcion_traducida = translator.translate(descripcion, dest='es')
        listado_cartas.append({
            'info': {
                'key': i['idName'],
                'synonyms': [
                    i['name'],
                ]
            },
            'title': i['name'],
            'description': i['description'],#str(descripcion_traducida.text),
            'image': {
                'imageUri': 'http://www.clashapi.xyz/images/cards/'+str(i['idName'])+'.png',
                'accessibilityText': str(i['idName'])
            }
        })
    return listado_cartas

def mazo_aleatorio(request):
    """action de mazo aleatorio
        Action que llama a la API para obtener un mazo aleatorio
    """

    mazo= get_mazo_aleatorio()
    listado_cartas = get_listado_cartas(mazo)
    #print(mazo)
    print('ESTO ES EL LISTADO DE CARTAS...')
    print(listado_cartas)
    result = {
        'fulfillmentText': 'este es el mazo resultante',
        'fulfillmentMessages': [
            {
                'platform': 'ACTIONS_ON_GOOGLE',
                'simpleResponses': {
                    'simpleResponses': [
                        {
                            'textToSpeech': 'este es el mazo resultante',
                            'displayText': 'Este es el mazo resultante',
                        }
                    ]
                }
            },
            {
                'platform': 'ACTIONS_ON_GOOGLE',
                'carouselSelect': {
                    'items': [i for i in listado_cartas]
                },
            },
        ],
    }
    respuesta = parsear_respuesta.parsear_respuesta(result)
    return respuesta
