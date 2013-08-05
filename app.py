import json
import os
import time
import urllib
import urlparse
from functools import wraps
from optparse import OptionParser

from flask import Flask, make_response, request

import defaults


LATENCY = 0
PER_PAGE = 5
app = Flask('Flue')


def _paginated(field, generator, result_count=24):
    page = int(request.args.get('offset', 0)) / PER_PAGE
    if page * PER_PAGE > result_count:
        items = []
    else:
        items = [gen for i, gen in
                 zip(xrange(min(10, result_count - page * PER_PAGE)),
                     generator())]

    next_page = None
    if (page + 1) * PER_PAGE <= result_count:
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
        next_page_qs['offset'] = (page + 1) * PER_PAGE
        next_page_qs['limit'] = PER_PAGE
        next_page = next_page + '?' + urllib.urlencode(next_page_qs)

    return {
        field: items,
        'meta': {
            'limit': PER_PAGE,
            'offset': PER_PAGE * page,
            'next': next_page,
            'total_count': result_count,
        },
    }


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
