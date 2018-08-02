#!/usr/bin/python3
# -*- coding: utf-8 -*-

import json
from flask import make_response


def parsear_respuesta(result):
    """
        Método para parsear la respuesta a json y poder enviarlo al lado cliente
    """
    res = json.dumps(result)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r