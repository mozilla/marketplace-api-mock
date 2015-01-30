import random
from cgi import escape
from datetime import datetime, timedelta

from mpconstants.collection_colors import COLLECTION_COLORS

COLLECTION_COLORS = COLLECTION_COLORS.items()


# XSS helpers.
XSS = False

xss_text = '"\'><script>alert("poop");</script><\'"'

def _text(default):
    return xss_text if XSS else default

dummy_text = 'foo bar zip zap cvan fizz buzz something something'.split()

counter = 0

AUTHORS = [
    _text('Lord Basta of the Iron Isles'),
    _text('Chris Van Halen'),
    _text('Ngo Way'),
    _text('Huck Charmston'),
    _text('Davor van der Beergulpen')
]

CARRIERS = [
    'america_movil',
    'kddi',
    'o2',
    'telefonica',
    'deutsche_telekom',
]

FEED_APP_TYPES = [
    'icon',
    'image',
    'description',
    'quote',
    'preview'
]

REGIONS = [
    'de',
    'es',
    'mx',
    'jp',
    'us'
]

MESSAGES = [
    ['be careful, cvan made it', 'loljk'],
    ["it's probably a game or something"],
    None
]

SCREENSHOT_MAP = [
    (126, 126144),
    (131, 131610),
    (92, 92498),
    (118, 118204)
]

SAMPLE_BG = '/media/img/logos/firefox-256.png'

# Mapping between special app slug to their ids.
SPECIAL_SLUGS_TO_IDS = {
    'installed': 414141,
    'developed': 424242,
    'purchased': 434343,
}

USER_NAMES = ['Von Cvan', 'Lord Basta', 'Ser Davor', 'Queen Krupa',
              'Le Ngoke']


def _rand_text(len=10):
    """Generate random string."""
    return _text(' '.join(random.choice(dummy_text) for i in xrange(len)))


def _app_preview():
    """Generate app preview object."""
    url = ('https://marketplace.cdn.mozilla.net/'
           'img/uploads/previews/%%s/%d/%d.png' %
           random.choice(SCREENSHOT_MAP))
    return {
        'caption': _rand_text(len=5),
        'filetype': 'image/png',
        'thumbnail_url': url % 'thumbs',
        'image_url': url % 'full',
    }


def _rand_bool():
    """Randomly returns True or False."""
    return random.choice((True, False))


def _carrier(**kw):
    return {
        'id': kw.get('id', 1),
        'name': kw.get('name', 'Seavan Sellular'),
        'resource_uri': kw.get('resource_uri',
                                   '/api/v1/services/carrier/seavan_sellular/'),
        'slug': random.choice(CARRIERS),
    }


def _category(slug, name):
    """Creates a category object."""
    return {
        'name': _text(name),
        'slug': slug,
    }


def _rand_datetime():
    """Randomly returns a datetime within the last 600 days."""
    rand_date = datetime.now() - timedelta(days=random.randint(0, 600))
    return rand_date.strftime('%Y-%m-%dT%H:%M:%S')


def _region(**kw):
    return {
        'id': kw.get('id', 1),
        'name': kw.get('name', 'Appistan'),
        'resource_uri': kw.get('resource_uri',
                                   '/api/v1/services/region/ap/'),
        'slug': random.choice(REGIONS),
        'default_currency': kw.get('default_currency', 'USD'),
        'default_language': kw.get('default_language', 'en-AP'),
    }


def _user_apps():
    """Returns user's apps object."""
    return {
        'installed': [SPECIAL_SLUGS_TO_IDS['installed']],
        'developed': [SPECIAL_SLUGS_TO_IDS['developed']],
        'purchased': [SPECIAL_SLUGS_TO_IDS['purchased']]
    }


def app(**kw):
    """
    In the API everything here except `user` should be serialized and keyed off
    counter:region:locale.
    """
    global counter
    counter += 1

    slug = kw.get('slug', 'app-%d' % counter)

    data = {
        'id': SPECIAL_SLUGS_TO_IDS.get(slug, counter),
        'author': random.choice(AUTHORS),
        'categories': ['social', 'games'],
        'content_ratings': {
            'body': 'generic',
            'rating': '12',
            'descriptors': ['scary', 'lang', 'drugs'],
            'interactives': ['users-interact', 'shares-info']
        },
        'current_version': _text('%d.0' % int(random.random() * 20)),
        'description': {'en-US': escape(kw.get('description',
                                                   _rand_text(100)))},
        'device_types': ['desktop', 'firefoxos', 'android-mobile',
                         'android-tablet'],
        'file_size': 12345,
        'homepage': 'http://marketplace.mozilla.org/',
        'icons': {
            64: '/media/img/logos/64.png'
        },
        'is_packaged': slug == 'packaged' or _rand_bool(),
        'manifest_url':
            'http://%s%s.testmanifest.com/manifest.webapp' %
            (_rand_text(1), random.randint(1, 50000)),  # Minifest if packaged
        'name': _text('App %d' % counter),
        'notices': random.choice(MESSAGES),
        'previews': [_app_preview() for i in range(4)],
        'privacy_policy': kw.get('privacy_policy', _rand_text()),
        'public_stats': False,
        'slug': slug,
        'ratings': {
            'average': random.random() * 4 + 1,
            'count': int(random.random() * 500),
        },
        'release_notes': kw.get('release_notes', _rand_text(100)),
        'support_email': _text('support@%s.com' % slug),
        'support_url': _text('support.%s.com' % slug),
        'upsell': False,
    }

    has_price = _rand_bool()
    price = '%.2f' % (random.random() * 10)
    if slug == 'free':
        has_price = False
    elif slug == 'paid':
        has_price = True
        price = '0.99'

    if slug == 'upsell':
        data['upsell'] = {
            'id': random.randint(1, 10000),
            'name': _rand_text(),
            'icon_url': '/media/img/logos/firefox-256.png',
            'app_slug': 'upsold',
            'resource_uri': '/api/v1/fireplace/app/%s/' % 'upsold',
        }

    if has_price:
        data.update(price=price, price_locale='$%s' % price)
    else:
        data.update(price=None, price_locale='$0.00')

    data['payment_required'] = has_price

    if slug == 'packaged':
        data['current_version'] = '1.0'

    data.update(app_user_data(slug))

    return dict(data, **kw)


def review_user_data(slug=None):
    data = {
        'user': {
            'has_rated': _rand_bool(),
            'can_rate': True,
        }
    }
    if data['user']['can_rate']:
        data['rating'] = random.randint(1, 5)
        data['user']['has_rated'] = _rand_bool()

    # Conditional slugs for great debugging.
    if slug == 'has_rated':
        data['user']['has_rated'] = True
        data['user']['can_rate'] = True
    elif slug == 'can_rate':
        data['user']['has_rated'] = False
        data['user']['can_rate'] = True
    elif slug == 'cant_rate':
        data['user']['can_rate'] = False

    return data


def app_user_data(slug=None):
    data = {
        'user': {
            'developed': _rand_bool(),
        }
    }
    # Conditional slugs for great debugging.
    if slug == 'developed':
        data['user']['developed'] = True
    elif slug == 'user':
        data['user']['developed'] = False

    return data


def app_user_review(slug, **kw):
    data = {
        'body': kw.get('review', _rand_text()),
        'rating': 4
    }
    return data


def review(**kw):
    global counter
    counter += 1

    version = None
    if _rand_bool():
        version = {
            'name': random.randint(1, 3),
            'latest': False,
        }

    return dict({
        'rating': random.randint(1, 5),
        'body': _rand_text(len=20),
        'created': _rand_datetime(),
        'is_flagged': random.randint(1, 5) == 1,
        'is_author': random.randint(1, 5) == 1,
        'modified': _rand_datetime(),
        'report_spam': '/api/v1/apps/rating/%d/flag/' % counter,
        'resource_uri': '/api/v1/apps/rating/%d/' % counter,
        'user': {
            'display_name': _text(random.choice(USER_NAMES)),
            'id': counter,
        },
        'version': version,
    }, **kw)


def feed_item(**kw):
    global counter
    counter += 1

    return dict({
        'app': feed_app(),
        'brand': brand(),
        'carrier': _carrier()['slug'],
        'collection': collection(),
        'id': counter,
        'item_type': random.choice(['app', 'collection', 'brand']),
        'url': '/api/v2/feed/items/%d/' % counter,
        'region': _region()['slug'],
        'shelf': shelf()
    }, **kw)


def feed_app(**kw):
    pullquote_text = '"' + _rand_text(len=12) + '"'
    description = random.choice([_rand_text(len=20), ''])
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

    return dict({
        'app_count': app_count,
        'apps': [app() for i in xrange(app_count)],
        'id': counter,
        'layout': random.choice(['list', 'grid']),
        'slug': 'brand-%d' % counter,
        'type': random.choice(['hidden-gem', 'music', 'travel']),
        'url': '/api/v2/feed/brand%d' % counter
    }, **kw)


def collection(**kw):
    global counter
    counter += 1

    slug = 'collection-%s' % counter
    rand_color = random.choice(COLLECTION_COLORS)
    app_count = kw.get('app_count', 6)

    data = {
        'name': _text('Collection %s' % counter),
        'id': counter,
        'slug': slug,
        'app_count': app_count,
        'type': 'listing',
        'description': random.choice([_rand_text(len=20), '']),
        'apps': [app() for i in xrange(app_count)],
        'background_color': rand_color[1],
        'color': rand_color[0],
        'icon': 'http://f.cl.ly/items/103C0e0I1d1Q1f2o3K2B/'
                'mkt-collection-logo.png',
        'url': '/api/v2/feed/collections/%d/' % counter
    }

    if _rand_bool():
        data['background_image'] = SAMPLE_BG,
        data['type'] = 'promo'

    data = dict(data, **kw)

    if data['slug'] == 'grouped':
        # Divide into three groups for mega collections.
        for i, _app in enumerate(data['apps']):
            if i < data['app_count'] / 3:
                _app['group'] = 'Group 1'
            elif i < data['app_count'] * 2 / 3:
                _app['group'] = 'Group 2'
            else:
                _app['group'] = 'Group 3'

    return data


def shelf(**kw):
    global counter
    counter += 1

    carrier = _carrier()['slug']
    app_count = kw.get('app_count', 6)

    data = {
        'apps': [app() for i in xrange(app_count)],
        'app_count': app_count,
        'background_image': SAMPLE_BG,
        'background_image_landing': SAMPLE_BG,
        'carrier': carrier,
        'description': '',
        'id': counter,
        'name': '%s Op Shelf' % carrier.replace('_', ' ').capitalize(),
        'region': 'restofworld',
        'slug': 'shelf-%d' % counter,
        'url': '/api/v2/feed/shelves/%d/' % counter
    }

    return dict(data, **kw)


def feed():
    """
    Generates a Feed, with at least one of every type of Feed module.
    Note that the existence of these Feed Items are tied to continuous
    integration such as the slugs for UA tracking. Keep in mind before
    changing.
    """
    data = [
        feed_item(item_type='shelf', shelf=shelf(name='Shelf')),
        feed_item(item_type='shelf', shelf=shelf(description=_rand_text(),
                                                 name='Shelf Description')),
        feed_item(item_type='brand', brand=brand(layout='grid',
                                                 slug='brand-grid')),
        feed_item(item_type='brand', brand=brand(layout='list',
                                                 slug='brand-list')),
        feed_item(item_type='collection',
                  collection=collection(type='promo',
                                        slug='grouped',
                                        name='Mega Collection'),
                                        background=SAMPLE_BG,
                                        description=_rand_text()),
        feed_item(item_type='collection',
                  collection=collection(type='promo',
                                        slug='coll-promo',
                                        name='Coll Promo')),
        feed_item(item_type='collection',
                  collection=collection(type='promo',
                                        slug='coll-promo-desc',
                                        name='Coll Promo Desc'),
                                        description=_rand_text()),
        feed_item(item_type='collection',
                  collection=collection(type='promo',
                                        slug='coll-promo-bg',
                                        name='Coll Promo Background'),
                                        background=SAMPLE_BG),
        feed_item(item_type='collection',
                  collection=collection(type='promo',
                                        slug='coll-promo-bg-desc',
                                        description=_rand_text(),
                                        name='Coll Promo Background Desc')),
        feed_item(item_type='collection',
                  collection=collection(type='listing',
                                        slug='coll-listing',
                                        name='Coll Listing')),
        feed_item(item_type='collection',
                  collection=collection(type='listing',
                                        slug='coll-listing-desc',
                                        description=_rand_text(),
                                        name='Coll Listing Desc')),
    ]

    for feed_app_type in FEED_APP_TYPES:
        data.append(feed_item(item_type='app',
                              app=feed_app(type=feed_app_type,
                                           slug='feedapp-%s' % feed_app_type)))

    return data


def preview():
    global counter
    counter += 1

    return {
        'id': counter,
        'position': 1,
        'thumbnail_url': 'http://f.cl.ly/items/103C0e0I1d1Q1f2o3K2B/'
                         'mkt-collection-logo.png',
        'image_url': SAMPLE_BG,
        'filetype': 'image/png',
        'resource_uri': 'pi/v1/apps/preview/%d' % counter
    }
