"""
Rocketfuel is where the publishing tool lives.
"""

import json

import app

DB = {
    'pk': 0,
    'collections': {},
}


def api_error(message, status_code=400):
    return app.make_response(json.dumps(message), status_code)


@app.route('/api/v1/rocketfuel/collections/', methods=['GET', 'POST'])
def collections_list():
    if app.request.method == 'POST':
        form = app.request.form
        DB['pk'] += 1
        return {
            'title': form.get('title'),
            'description': form.get('description'),
            'id': DB['pk'],
            'apps': [],
            'collection_type': form.get('collection_type'),
            'category': form.get('category'),
            'region': form.get('region'),
        }

    def gen():
        i = 0
        while 1:
            yield app.defaults.collection('Collection', 'collection-%d' % i)
            i += 1

    query = app.request.args.get('q')
    data = app._paginated('objects', gen, 0 if query == 'empty' else 24)
    return data


@app.route('/api/v1/rocketfuel/collections/<slug>/', methods=['GET', 'PATCH'])
def collections_get(slug):
    return app.defaults.collection('Collection %s' % slug, slug)


def _validate_app(app_id, slug):
    if not app_id:
        return api_error({'detail': '`app` was not provided.'})

    if app_id in DB['collections'].get(slug, []):
        return api_error({'detail': '`app` already exists in collection.'})


@app.route('/api/v1/rocketfuel/collections/<slug>/add_app/', methods=['POST'])
def collections_add_app(slug):
    app_id = app.request.form.get('app')

    _validate_app(app_id, slug)

    DB['collections'].setdefault(slug, []).append(app_id)

    collection = app.defaults.collection('Collection %s' % slug, slug)
    collection.update(apps=['/api/v1/apps/app/%s/' % app_id])

    return collection


@app.route('/api/v1/rocketfuel/collections/<slug>/remove_app/', methods=['POST'])
def collections_remove_app(slug):
    app_id = app.request.form.get('app')

    _validate_app(app_id, slug)

    # Uncomment if you want things to behave as they would with the real API.
    # if app_id not in DB['collections'].get(slug, []):
    #     return api_error({'detail': '`app` does not exist in collection.'})

    try:
        DB['collections'].get(slug, []).remove(app_id)
    except ValueError:
        pass

    collection = app.defaults.collection('Collection %s' % slug, slug)
    collection.update(apps=[])

    return collection


@app.route('/api/v1/rocketfuel/collections/<slug>/reorder_app/', methods=['POST'])
def collections_reorder_app(slug):
    app_id = app.request.form.get('app')
    position = app.request.form.get('position')

    _validate_app(app_id, slug)

    # Uncomment if you want things to behave as they would with the real API.
    # if app_id not in DB['collections'].get(slug, []):
    #     return api_error({'detail': '`app` does not exist in collection.'})

    if not position:
        return api_error({'detail': '`position` was not provided.'})

    return app.defaults.collection('Collection %s' % slug, slug)
