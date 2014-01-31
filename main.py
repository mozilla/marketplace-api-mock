"""
Flue is a simple application which mocks out the APIs used by Fireplace.
Pointing your instance of Fireplace using settings.js will allow you to
quickly get up and running without needing your own installation of Zamboni
or without needing to use -dev (offline mode).
"""

import json
import random

from flask import make_response, request

import app

import defaults
import persona
import rocketfuel
import services


@app.route('/api/v1/account/login/', methods=['POST'])
def login():
    assertion = request.form.get('assertion')
    audience = request.form.get('audience')
    is_native = int(request.form.get('is_native'))

    print 'Attempting verification:', audience, is_native

    email = persona.verify_assertion(assertion, audience, is_native)
    if not email:
        return make_response('{"error": "bad_assertion"}', 403)

    # At this point, we know that the user is a valid user.

    return {
        'error': None,
        'token': persona.get_token(email),
        'settings': {
            'display_name': email.split('@')[0],
            'email': email,
            'region': 'us',
        },
        'permissions': {}
    }


@app.route('/api/v1/account/settings/mine/', methods=['GET', 'PATCH'])
def settings():
    return {
        'display_name': 'Joe User',
        'email': request.args.get('email'),
        'region': 'us',
    }


@app.route('/api/v1/abuse/app/', methods=['POST'])
def app_abuse():
    if not request.form.get('text'):
        return {'error': True}
    return {'error': False}


@app.route('/api/v1/account/feedback/', methods=['POST'])
def feedback():
    if not request.form.get('feedback'):
        return {'error': True}
    return {'error': False}


@app.route('/api/v1/apps/app/<slug>/privacy/', methods=['GET'])
def privacy(slug):
    return {
        'privacy_policy': defaults.ptext(),
    }


@app.route('/api/v1/apps/category/')
def categories():
    return {
        'objects': [
            defaults.category('shopping', 'Shopping'),
            defaults.category('games', 'Games'),
            defaults.category('productivity', 'Productivity'),
            defaults.category('social', 'Social'),
            defaults.category('music', 'Music'),
            defaults.category('lifestyle', 'Thug Life'),
        ]
    }


@app.route('/api/v1/account/installed/mine/')
def installed():
    def gen():
        i = 0
        while 1:
            yield defaults.app('Purchased App', 'purchase%d' % i)
            i += 1

    query = request.args.get('q')
    data = app._paginated('objects', gen, 0 if query == 'empty' else 25)
    return data


@app.route('/api/v1/apps/search/')
def search():
    def gen():
        i = 0
        while 1:
            yield defaults.app('Result', 'sr%d' % i)
            i += 1

    query = request.args.get('q')
    data = app._paginated('objects', gen, 0 if query == 'empty' else 25)
    return data


@app.route('/api/v1/fireplace/search/featured/')
def category():
    def gen():
        i = 0
        while 1:
            yield defaults.app('Category Item', 'catm %d' % i)
            i += 1

    data = app._paginated('objects', gen)
    data['collections'] = [
        defaults.collection('Collection', 'collection-0',
                            collection_type=0),
        defaults.collection('Collection', 'collection-1',
                            collection_type=0),
    ]
    data['featured'] = [
        defaults.collection('Featured', 'featured', collection_type=1),
    ]
    data['operator'] = [
        defaults.collection('Operator Shelf', 'operator', collection_type=2),
    ]
    return data


@app.route('/api/v1/apps/rating/', methods=['GET', 'POST'])
def app_ratings():
    if request.method == 'POST':
        return {'error': False}

    def gen():
        i = 0
        while 1:
            yield defaults.rating()
            i += 1

    slug = request.form.get('app') or request.args.get('app')

    data = app._paginated('objects', gen)
    data['info'] = {
        'slug': slug,
        'average': random.random() * 4 + 1,
    }
    data.update(defaults.app_user_data(slug))
    return data


@app.route('/api/v1/apps/rating/<id>/', methods=['GET', 'PUT', 'DELETE'])
def app_rating(id):
    if request.method in ('PUT', 'DELETE'):
        return {'error': False}

    return defaults.rating()


@app.route('/api/v1/apps/rating/<id>/flag/', methods=['POST'])
def app_rating_flag(id):
    return ''


@app.route('/api/v1/fireplace/app/<slug>/')
def app_(slug):
    return defaults.app('Something something %s' % slug, slug)


@app.route('/api/v1/installs/record/', methods=['POST'])
def record_free():
    return {'error': False}


@app.route('/api/v1/receipts/install/', methods=['POST'])
def record_paid():
    return {'error': False}


@app.route('/api/v1/apps/<id>/statistics/', methods=['GET', 'POST'])
def app_stats(id):
    return json.loads(open('./fixtures/3serieschart.json', 'r').read())

@app.route('/api/v1/fireplace/consumer-info/', methods=['GET'])
def consumer_info():
    return {
        'region': 'us',
        'installed': [],
        'developed': [],
        'purchased': [],
    }


if __name__ == '__main__':
    app.run()
