#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import parsear_respuesta

def action_despedida(req=None):
    """action de despedida
        Accion de despedida para despedir al usuario de la aplicación
    """
    result = {
        'fulfillmentMessages': [
            {
                'platform': 'ACTIONS_ON_GOOGLE',
                'simpleResponses': {
                    'simpleResponses': [
                        {
                            'textToSpeech': 'Gracias por utilizar la aplicación de Clash Royale Decks',
                            "displayText": 'Gracias por utilizar la aplicación de Clash Royale Decks',
                        }
                    ]
                }
            },
        ],
    }
    respuesta = parsear_respuesta.parsear_respuesta(result)
    return respuesta