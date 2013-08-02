import json
import os
import time
from functools import wraps
from optparse import OptionParser

from flask import Flask, make_response

import defaults

LATENCY = 0
app = Flask('Flue')


# Monkeypatching for CORS and JSON.
ar = app.route


@wraps(ar)
def route(*args, **kwargs):
    methods = kwargs.get('methods') or ['GET']

    def decorator(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            resp = func(*args, **kwargs)
            if isinstance(resp, (dict, list, tuple, str, unicode)):
                resp = make_response(json.dumps(resp, indent=2), 200)
            resp.headers['Access-Control-Allow-Origin'] = '*'
            resp.headers['Access-Control-Allow-Methods'] = ','.join(methods)
            resp.headers['Access-Control-Allow-Headers'] = (
                'API-Filter, X-HTTP-METHOD-OVERRIDE')
            resp.headers['Content-type'] = 'application/json'
            if LATENCY:
                time.sleep(LATENCY)
            return resp

        if 'methods' in kwargs:
            kwargs['methods'].append('OPTIONS')

        registered_func = ar(*args, **kwargs)(wrap)
        registered_func._orig = func
        return registered_func

    return decorator



def run():
    parser = OptionParser()
    parser.add_option('--port', dest='port',
        help='port', metavar='PORT', default=os.getenv('PORT', '5000'))
    parser.add_option('--host', dest='hostname',
        help='hostname', metavar='HOSTNAME', default='0.0.0.0')
    parser.add_option('--latency', dest='latency',
        help='latency (sec)', metavar='LATENCY', default=0)
    parser.add_option('--xss', dest='xss',
        help='xss?', metavar='XSS', default=0)
    options, args = parser.parse_args()
    app.debug = True

    global LATENCY
    LATENCY = int(options.latency)

    if options.xss:
        defaults.XSS = bool(options.xss)
    app.run(host=options.hostname, port=int(options.port))
