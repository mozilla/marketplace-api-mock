"""
Generate Feed-related objects.
"""
import random

from mpconstants.collection_colors import COLLECTION_COLORS

from factory import app, carrier, preview, region
from factory.constants import AUTHORS, SAMPLE_BG
from factory.utils import rand_bool, rand_text, text


counter = 0

COLLECTION_COLORS = COLLECTION_COLORS.items()

FEED_APP_TYPES = [
    'icon',
    'image',
    'description',
    'quote',
    'preview'
]


def feed_item(**kw):
    global counter
    counter += 1

    return dict({
        'app': feed_app(),
        'brand': brand(),
        'carrier': carrier()['slug'],
        'collection': collection(),
        'id': counter,
        'item_type': random.choice(['app', 'collection', 'brand']),
        'url': '/api/v2/feed/items/%d/' % counter,
        'region': region()['slug'],
        'shelf': shelf()
    }, **kw)


def feed_app(**kw):
    pullquote_text = '"' + rand_text(n=12) + '"'
    description = random.choice([rand_text(n=20), ''])
    feedapp_type = random.choice(FEED_APP_TYPES)
    rand_color = random.choice(COLLECTION_COLORS)

    return dict({
        'app': app(),
        'background_color': rand_color[1],
        'color': rand_color[0],
        'description': description,
        'type': FEED_APP_TYPES[0],
        'background_image': SAMPLE_BG,
        'id': counter,
        'preview': preview(),
        'pullquote_attribute': random.choice(AUTHORS),
        'pullquote_rating': random.randint(1, 5),
        'pullquote_text': pullquote_text,
        'slug': 'feed-app-%d' % counter,
        'url': '/api/v2/feed/apps/%d' % counter
    }, **kw)


def brand(**kw):
    global counter
    counter += 1

    app_count = kw.get('app_count', 6)

    data = {
        'app_count': app_count,
        'apps': [app() for i in xrange(app_count)],
        'id': counter,
        'layout': random.choice(['list', 'grid']),
        'slug': 'brand-%d' % counter,
        'type': random.choice(['hidden-gem', 'music', 'travel']),
        'url': '/api/v2/feed/brand%d' % counter
    }

    data = dict(data, **kw)

    if data['slug'] == 'brand-grid':
        data.update({
            'layout': 'grid'
        })
    elif data['slug'] == 'brand-list':
        data.update({
            'layout': 'list'
        })

    return data


def collection(**kw):
    global counter
    counter += 1

    slug = 'collection-%s' % counter
    rand_color = random.choice(COLLECTION_COLORS)
    app_count = kw.get('app_count', 6)

    data = {
        'name': text('Collection %s' % counter),
        'id': counter,
        'slug': slug,
        'app_count': app_count,
        'type': 'listing',
        'description': random.choice([rand_text(n=20), '']),
        'apps': [app() for i in xrange(app_count)],
        'background_color': rand_color[1],
        'color': rand_color[0],
        'icon': 'http://f.cl.ly/items/103C0e0I1d1Q1f2o3K2B/'
                'mkt-collection-logo.png',
        'url': '/api/v2/feed/collections/%d/' % counter
    }

    if rand_bool():
        data['background_image'] = SAMPLE_BG,
        data['type'] = 'promo'

    data = dict(data, **kw)

    if data['slug'] == 'grouped':
        # Divide into three groups for mega collections.
        data.update({
            'background_image': SAMPLE_BG,
            'description': rand_text(),
            'name': 'Mega Collection',
            'type': 'promo'
        })
        for i, _app in enumerate(data['apps']):
            if i < data['app_count'] / 3:
                _app['group'] = 'Group 1'
            elif i < data['app_count'] * 2 / 3:
                _app['group'] = 'Group 2'
            else:
                _app['group'] = 'Group 3'
    elif data['slug'] == 'coll-promo':
        data.update({
            'name': 'Coll Promo',
            'type': 'promo',
        })
    elif data['slug'] == 'coll-promo-desc':
        data.update({
            'description': rand_text(),
            'name': 'Coll Promo Desc',
            'type': 'promo',
        })
    elif data['slug'] == 'coll-promo-bg':
        data.update({
            'background_image': SAMPLE_BG,
            'name': 'Coll Promo Background',
            'type': 'promo',
        })
    elif data['slug'] == 'coll-promo-bg-desc':
        data.update({
            'background_image': SAMPLE_BG,
            'description': rand_text(),
            'name': 'Coll Promo Background Desc',
            'type': 'promo',
        })
    elif data['slug'] == 'coll-listing':
        data.update({
            'name': 'Coll Listing',
            'type': 'listing',
        })
    elif data['slug'] == 'coll-listing-desc':
        data.update({
            'description': rand_text(),
            'name': 'Coll Listing Desc',
            'type': 'listing',
        })

    return data


def shelf(**kw):
    global counter
    counter += 1

    _carrier = carrier()['slug']
    app_count = kw.get('app_count', 6)

    data = {
        'apps': [app() for i in xrange(app_count)],
        'app_count': app_count,
        'background_image': SAMPLE_BG,
        'background_image_landing': SAMPLE_BG,
        'carrier': _carrier,
        'description': '',
        'id': counter,
        'name': '%s Op Shelf' % _carrier.replace('_', ' ').capitalize(),
        'region': 'restofworld',
        'slug': 'shelf-%d' % counter,
        'url': '/api/v2/feed/shelves/%d/' % counter
    }

    data = dict(data, **kw)

    if data['slug'] == 'shelf':
        data.update({
            'name': 'Shelf'
        })
    elif data['slug'] == 'shelf-desc':
        data.update({
            'description': rand_text(),
            'name': 'Shelf Description'
        })

    return data


def feed():
    """
    Generates a Feed, with at least one of every type of Feed module.
    Note that the existence of these Feed Items are tied to continuous
    integration such as the slugs for UA tracking. Keep in mind before
    changing.
    """
    data = [
        feed_item(item_type='shelf',
                  shelf=shelf(slug='shelf')),
        feed_item(item_type='shelf',
                  shelf=shelf(slug='shelf-desc')),
        feed_item(item_type='brand',
                  brand=brand(slug='brand-grid')),
        feed_item(item_type='brand',
                  brand=brand(slug='brand-list')),
        feed_item(item_type='collection',
                  collection=collection(slug='grouped')),
        feed_item(item_type='collection',
                  collection=collection(slug='coll-promo')),
        feed_item(item_type='collection',
                  collection=collection(slug='coll-promo-desc')),
        feed_item(item_type='collection',
                  collection=collection(slug='coll-promo-bg')),
        feed_item(item_type='collection',
                  collection=collection(slug='coll-promo-bg-desc')),
        feed_item(item_type='collection',
                  collection=collection(slug='coll-listing')),
        feed_item(item_type='collection',
                  collection=collection(slug='coll-listing-desc')),
    ]

    for feed_app_type in FEED_APP_TYPES:
        data.append(feed_item(item_type='app',
                              app=feed_app(type=feed_app_type,
                                           slug='feedapp-%s' % feed_app_type)))

    return data
