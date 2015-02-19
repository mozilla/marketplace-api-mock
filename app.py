import json
import os
import sys
import time
import traceback
import urllib
import urlparse
from functools import wraps
from optparse import OptionParser

from flask import Flask, make_response, request, Response

import factory


LATENCY = 0
PER_PAGE = 25
Response.default_mimetype = 'application/json'

app = Flask('Flue', static_url_path='/fireplace')


def _paginated(field, generator, result_count=42, objects=None, **kw):
    per_page = int(request.args.get('limit', PER_PAGE))
    page = int(request.args.get('offset', 0)) / per_page
    if page * per_page > result_count:
        items = []
    elif objects:
        items = objects
    else:
        items = [gen for i, gen in
                 zip(xrange(min(per_page, result_count - page * per_page)),
                     generator(**kw))]

    next_page = None
    if (page + 1) * per_page <= result_count:
        next_page = request.url
        next_page = next_page[len(request.base_url) -
                              len(request.path + request.script_root):]
        if '?' in next_page:
            next_page_qs = urlparse.parse_qs(
                next_page[next_page.index('?') + 1:],
                keep_blank_values=True)
            next_page_qs = dict(zip(next_page_qs.keys(),
                                    [x[0] for x in next_page_qs.values()]))
            next_page = next_page[:next_page.index('?')]
        else:
            next_page_qs = {}
        next_page_qs['offset'] = (page + 1) * per_page
        next_page_qs['limit'] = per_page
        next_page = next_page + '?' + urllib.urlencode(next_page_qs)

    return {
        field: items,
        'meta': {
            'limit': per_page,
            'offset': per_page * page,
            'next': next_page,
            'total_count': result_count,
        },
    }


# Monkeypatching for CORS and JSON.
ar = app.route


def inject_cors_headers(response, methods=None):
    allow_methods = set([request.method] if methods is None else methods)
    allow_methods.add('OPTIONS')
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = ','.join(allow_methods)
    response.headers['Access-Control-Allow-Headers'] = (
        'API-Filter, X-HTTP-METHOD-OVERRIDE')


@wraps(ar)
def route(*args, **kwargs):
    methods = kwargs.get('methods') or ['GET']

    def decorator(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            resp = func(*args, **kwargs)
            if isinstance(resp, (dict, list, tuple, str, unicode)):
                resp = make_response(json.dumps(resp, indent=2), 200)
            inject_cors_headers(resp, methods)
            if LATENCY:
                time.sleep(LATENCY)
            return resp

        if 'methods' in kwargs:
            kwargs['methods'].append('OPTIONS')

        registered_func = ar(*args, **kwargs)(wrap)
        registered_func._orig = func
        return registered_func

    return decorator


@app.errorhandler(404)
def handler404(err):
    response = make_response(err, 404)
    inject_cors_headers(response)
    return response


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
    parser.add_option('--no-debug', dest='debug', action='store_false',
        help='disable debug mode', default=True)
    options, args = parser.parse_args()
    if options.debug:
        app.debug = True
    else:
        @app.errorhandler(500)
        def error(error):
            exc_type, exc_value, tb = sys.exc_info()
            content = ''.join(traceback.format_tb(tb))
            response = make_response(content, 500)
            inject_cors_headers(response)
            return response

    global LATENCY
    LATENCY = int(options.latency)

    if options.xss:
        factory.XSS = bool(options.xss)
    app.run(host=options.hostname, port=int(options.port))
