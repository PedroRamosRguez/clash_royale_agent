def set_card_details(mensaje_voz, card, listado_sugerencias):
    card_picture = 'http://www.clashapi.xyz/images/cards/'+str(card['idName'])+'.png',
    simple_card = {
        "fulfillmentMessages": [
            {
                'platform': 'ACTIONS_ON_GOOGLE',
                'simple_responses': {
                    'simple_responses': [
                        {
                            'text_to_speech': mensaje_voz,
                            'display_text': ' '
                        }
                    ]
                }
            },
            {
                'platform': 'ACTIONS_ON_GOOGLE',
                'basic_card': {
                    'title': card['name'],
                    'formatted_text': card['description'],
                    'image': {
                        'image_uri': card_picture,
                        'accessibilityText': card['name'],
                    },
                }
            },
            {
                'platform': 'ACTIONS_ON_GOOGLE',
                'suggestions': {
                    'suggestions': listado_sugerencias
                }
            },
        ]
    }
    return simple_card
