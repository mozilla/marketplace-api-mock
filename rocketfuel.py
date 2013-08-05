"""
Rocketfuel is where the publishing tool lives.
"""

import app

pk = 0


@app.route('/api/v1/rocketfuel/collections/', methods=['GET', 'POST'])
def collections_list():
    global pk

    if app.request.method == 'POST':
        form = app.request.form
        pk += 1
        return {
            'name': form.get('name'),
            'description': form.get('description'),
            'id': pk,
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
