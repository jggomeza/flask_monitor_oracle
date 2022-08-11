#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import socket
import sys
from app import create_app

os.environ["FLASK_CONFIG"] = os.getenv('FLASK_CONFIG') or 'default'
app = create_app(os.getenv('FLASK_CONFIG'))
hostname=socket.gethostname()   
IPAddr=socket.gethostbyname(hostname)   
 


# No se toca este metodo
# asi se ejecuta
# python app.py -h 127.0.0.1 -p 5020 -b True
if __name__ == "__main__":
    arg = sys.argv
    host = IPAddr
    port = 5020
    debug = True
    
    if arg.count("-h") > 0:
        try:
            host = str(arg[arg.index("-h") + 1]) if arg[arg.index("-h") + 1] else '127.0.0.1'
        except:
            host = '127.0.0.1'
    if arg.count("-p") > 0:
        try:
            port = arg[arg.index("-p") + 1] if arg[arg.index("-p") + 1] else 5000
        except:
            port = 5000
    if arg.count("-b") > 0:
        try:
            debug = bool(str(arg[arg.index("-b") + 1]).capitalize())
        except:
            debug = False

    app.run(host=host, port=port, debug=debug, threaded=True)

