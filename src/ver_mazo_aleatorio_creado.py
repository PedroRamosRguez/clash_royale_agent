def show_created_deck(random_created_deck):
    """
        Función que se ejecuta si se ha creado un mazo aleatorio, sirve para volver a ver el mazo creado
        en caso de que se esté viendo una carta en detalle del mismo mazo.
    """
    elixir_cost = [i for i in random_created_deck['elixirCost']]
    arenas = [i for i in random_created_deck['arena']]
    average_elixir_cost = round(sum(elixir_cost)/ len(elixir_cost))
    top_arena = max(arenas)
    voice_message = ''.join('''<speak><emphasis level='strong'>
    este es el mazo resultante: <break time='500ms'/> <break time='500ms'/>''')
    for i in random_created_deck['card_list']:
        voice_message = voice_message + '''{}<break time='500ms'/>'''.format(i['title'])
    voice_message = voice_message + '''.Tiene una media de coste de elixir de {}
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
                    'items': [i for i in random_created_deck['card_list']]
                },

            },
        ],
    }
    return result
