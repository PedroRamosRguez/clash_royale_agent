#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from flask import Flask
# Flask app should start in global layout
app = Flask(__name__)
@app.route('/')
def hello_world():
   return 'hola mundo'

if __name__ == '__main__':
    port = int(os.getenv('PORT', 50000))
    print("Aplicacion funcionando en el puerto %d" % port)
    app.run(debug=True, port=port, host='0.0.0.0')