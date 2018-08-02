#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import parsear_respuesta

def get_sugerencias():
    """Metodo para obtener las sugerencias de la bienvenida al bot
       Se añadió como método para que sea dinámico, es decir se puedan
       añadir o eliminar en caso de que se actualicen las actions creadas
       en el bot
    """
    sugerencias = [
        {
            'title': 'Información sobre cartas'
        },
        {
            'title': 'Crear mazo aleatorio'
        },
    ]
    return sugerencias

def action_bienvenida(req=None):
    """action de bienvenida
        Action que se ejecuta para dar la bienvenida a los usuarios.
    """
    sugerencias_bienvenida = get_sugerencias()
    mensaje_sugerencias = ["<break time='500ms'/>"+str(i['title']) for i in sugerencias_bienvenida]
    mensaje_bienvenida_mostrar = '''
        ¡Hola! Bienvenido, soy un agente para ayudarte en el juego clash royale,¿qué información deseas ver?
    '''
    mensaje_bienvenida_escuchar = '''<speak><emphasis level='strong'>
        ¡Hola! Bienvenido, soy un agente para ayudar en el juego clash royale,¿qué información deseas ver?
    '''
    for i in mensaje_sugerencias:
        mensaje_bienvenida_escuchar = mensaje_bienvenida_escuchar + str(i)+','
    mensaje_bienvenida_escuchar = mensaje_bienvenida_escuchar + '''</emphasis></speak>'''
    result = {
        'fulfillmentMessages': [
            {
                'platform': 'ACTIONS_ON_GOOGLE',
                'simpleResponses': {
                    'simpleResponses': [
                        {
                            'textToSpeech': mensaje_bienvenida_escuchar,
                            "displayText": mensaje_bienvenida_mostrar,
                        }
                    ]
                }
            },
            {
                'platform': 'ACTIONS_ON_GOOGLE',
                'suggestions': {
                    'suggestions': sugerencias_bienvenida,
                }
            },
        ],
    }
    respuesta = parsear_respuesta.parsear_respuesta(result)
    return respuesta