import urllib
import urlparse
from functools import wraps

from flask import jsonify, make_response, request, Flask, Response


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


def set_cors_headers(response, methods):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = ','.join(methods)
    response.headers['Access-Control-Allow-Headers'] = (
        'API-Filter, X-HTTP-METHOD-OVERRIDE')


def cors_route(*args, **kwargs):
    def wrap(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            response = fn(*args, **kwargs)
            set_cors_headers(response)
            return response
        return app.route(*args, **kwargs)(inner)
    return wrap


def as_json(data, methods):
    response = jsonify(data)
    set_cors_headers(response, methods)
    return response


def route_as_json(*args, **kwargs):
    methods = kwargs.get('methods')
    cors_methods = set(methods or [])
    cors_methods.add('OPTIONS')

    def wrap(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            data = fn(*args, **kwargs)
            cors_methods.add(request.method)
            return as_json(data, methods=cors_methods)
        return app.route(*args, **kwargs)(inner)
    return wrap


@app.errorhandler(404)
def handler404(err):
    response = make_response(err, 404)
    set_cors_headers(response, [request.method])
    return response
