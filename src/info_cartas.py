import parsear_respuesta
from mazo_aleatorio import get_selected_card
from simpleCard import set_card_details
from sugerencias import escuchar_sugerencias

def get_sugerencias():
    sugerencias = [
        {
            'title': 'Generar mazo aleatorio',
        },
        {
            'title': 'Salir',
        },
    ]
    return sugerencias
def set_card_selected(card_selected):
    """
        Función para crear la card de dialogflow con la informacion detallada de la carta seleccionada del mazo aleatorio creado.
    """
    listado_sugerencias = get_sugerencias()
    speech_sugerencias = escuchar_sugerencias(listado_sugerencias)
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
    card_details = set_card_details(
        mensaje_voz,
        mensaje_card,
        card_selected,
        listado_sugerencias
    )
    return card_details
def info_cartas(req):
    """
        Funcion que es llamada cuando se activa la action de informacion sobre cartas.
    """
    print('esta es la action de la informacion de las cartas')
    carta = req['queryResult']['parameters']['Cartas'] or req['queryResult']['outputContexts'][0]['parameters']['Cartas.original']
    print(carta)
    info_carta = get_selected_card(carta)
    if 'error' in info_carta:
        resultado = {
           'fulfillmentMessages': [
                {
                    'platform': 'ACTIONS_ON_GOOGLE',
                    'simpleResponses': {
                        'simpleResponses': [
                            {
                                'textToSpeech': 'No existe información sobre la carta {}'.format(carta),
                                'displayText': 'No existe información sobre la carta {}'.format(carta),
                            }
                        ]
                    }
                }, 
            ] 
        }
        respuesta = parsear_respuesta.parsear_respuesta(resultado)
    else:
        resultado = set_card_selected(info_carta)
        respuesta = parsear_respuesta.parsear_respuesta(resultado)
    return respuesta