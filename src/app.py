#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import bienvenida
import despedida
import info_cartas
import mazo_aleatorio

from api_cards_espanol import *
from flask import Flask
from flask import request
from flask_restful import Api
# Flask app should start in global layout
app = Flask(__name__)
log = app.logger
app.register_blueprint(api_card_espaniol)
#objeto donde se añaden las acciones del agente
actions = {
    'bienvenida': bienvenida.action_bienvenida,
    'card_detalle': mazo_aleatorio.card_detail,
    'despedida': despedida.action_despedida,
    'info_carta':info_cartas.info_cartas,
    'mazo_aleatorio': mazo_aleatorio.random_deck,
    'ver_mazo_creado': mazo_aleatorio.deck_created,
    
}

@app.route('/status', methods=['GET'])
def status():
    """Comprobar el status del bot"""
    return 'OK'

@app.route('/static_reply', methods=['POST'])
def static_reply():
    """
        Función que se carga para devolver la respuesta al usuario
    """
    global actions
    req = request.get_json(silent=True, force=True)
    print(req['queryResult']['languageCode'])
    try:
        action = req['queryResult']['action']
    except AttributeError:
        return 'json error'
    if action in actions:
        functor = actions[action]
        if functor.__doc__:
            print(functor.__doc__.split('\n')[0])
        respuesta = functor(req)
    else:
        log.error('no esta dentro de las actions')
    return respuesta

#importar modulo de la api

if __name__ == '__main__':
    port = int(os.getenv('PORT', 50000))
    print("Aplicacion funcionando en el puerto %d" % port)
    app.run(debug=True, port=port, host='0.0.0.0')
