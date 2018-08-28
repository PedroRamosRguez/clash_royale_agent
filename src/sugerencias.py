#!/usr/bin/python3
# -*- coding: utf-8 -*-

def escuchar_sugerencias(sugerencias):
    """
        Método para añadir las sugerencias al mensaje de voz
    """
    speech_sugerencias = ''
    for i in sugerencias:
        speech_sugerencias = speech_sugerencias + i['title'] + ', '
    return speech_sugerencias