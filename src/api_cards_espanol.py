from flask import Flask, jsonify, abort, make_response, Blueprint
import cards

api_card_español = Blueprint('api_card_español', __name__)
@api_card_español.route('/status/api/',methods=['GET'])
def status_api():
    return 'OK'

@api_card_español.route('/api/card/', methods=['GET'])
def get_cards():
    """
        Función para obtener toda la información de las cartas de la API
    """
    return jsonify(cards.cards)


@api_card_español.route('/api/card/<string:idName>', methods=['GET'])
def get_card(idName):
    """
        Función para obtener carta específica en la API
    """
    card = [card for card in cards.cards if card['idName'] == idName]
    if len(card) == 0:
        abort(404)
    return jsonify(card[0])

@api_card_español.errorhandler(404)
def not_found(error):
    """ Función para manejar el error en caso de no encontrar la carta en la API"""

    return make_response(jsonify({'error': 'Carta no encontrada'}), 404)
    