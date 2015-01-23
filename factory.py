import random
from cgi import escape
from datetime import datetime, timedelta


XSS = False

xss_text = '"\'><script>alert("poop");</script><\'"'
dummy_text = 'foo bar zip zap cvan fizz buzz something something'.split()


def text(default):
    return xss_text if XSS else default


def ptext(len=10):
    return text(' '.join(random.choice(dummy_text) for i in xrange(len)))


def rand_bool():
    return random.choice((True, False))


def category(slug, name):
    return {
        'name': text(name),
        'slug': slug,
    }

AUTHORS = [
    text('Lord Basta of the Iron Isles'),
    text('Chris Van Halen'),
    text('Kevin Ngo'),
    text('Chuck Harmston'),
    text('Davor van der Beergulpen')
]

CARRIERS = [
    'america_movil',
    'kddi',
    'o2',
    'telefonica',
    'deutsche_telekom',
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

# Mapping between special app slug to their ids.
SPECIAL_SLUGS_TO_IDS = {
    'installed': 414141,
    'developed': 424242,
    'purchased': 434343,
}

COLLECTION_COLORS = {
    'ruby': '#CE001C',
    'amber': '#F78813',
    'emerald': '#00953F',
    'topaz': '#0099D0',
    'sapphire': '#1E1E9C',
    'amethyst': '#5A197E',
    'garnet': '#A20D55',
}.items()

FEED_APP_TYPES = [
    'icon',
    'image',
    'description',
    'quote',
    'preview'
]

SAMPLE_BG_IMAGE = '/media/img/logos/firefox-256.png'


def _user_apps():
    return {
        'installed': [SPECIAL_SLUGS_TO_IDS['installed']],
        'developed': [SPECIAL_SLUGS_TO_IDS['developed']],
        'purchased': [SPECIAL_SLUGS_TO_IDS['purchased']]
    }


def _app_preview():
    url = ('https://marketplace.cdn.mozilla.net/'
           'img/uploads/previews/%%s/%d/%d.png' %
               random.choice(SCREENSHOT_MAP))
    return {
        'caption': ptext(len=5),
        'filetype': 'image/png',
        'thumbnail_url': url % 'thumbs',
        'image_url': url % 'full',
    }


def app(name, slug, **kwargs):
    # In the API everything here except `user` should be serialized and
    # keyed off app_id:region:locale.
    data = {
        'id': SPECIAL_SLUGS_TO_IDS.get(slug, random.randint(1, 40000)),
        'author': random.choice(AUTHORS),
        'categories': ['social', 'games'],
        'content_ratings': {
            'body': 'generic',
            'rating': '12',
            'descriptors': ['scary', 'lang', 'drugs'],
            'interactives': ['users-interact', 'shares-info']
        },
        'current_version': text('%d.0' % int(random.random() * 20)),
        'description': {'en-US': escape(kwargs.get('description',
                                                   ptext(100)))},
        'device_types': ['desktop', 'firefoxos', 'android-mobile',
                         'android-tablet'],
        'homepage': 'http://marketplace.mozilla.org/',
        'icons': {
            64: '/media/img/logos/64.png'
        },
        'is_packaged': slug == 'packaged' or rand_bool(),
        'manifest_url':
            'http://%s%s.testmanifest.com/manifest.webapp' %
            (ptext(1), random.randint(1, 50000)),  # Minifest if packaged
        'name': text(name),
        'notices': random.choice(MESSAGES),
        'previews': [_app_preview() for i in range(4)],
        'privacy_policy': kwargs.get('privacy_policy', ptext()),
        'public_stats': False,
        'slug': slug,
        'ratings': {
            'average': random.random() * 4 + 1,
            'count': int(random.random() * 500),
        },
        'release_notes': kwargs.get('release_notes', ptext(100)),
        'support_email': text('support@%s.com' % slug),
        'support_url': text('support.%s.com' % slug),
        'upsell': False,
    }

    has_price = rand_bool()
    price = '%.2f' % (random.random() * 10)
    if slug == 'free':
        has_price = False
    elif slug == 'paid':
        has_price = True
        price = '0.99'

    if slug == 'upsell':
        data['upsell'] = {
            'id': random.randint(1, 10000),
            'name': ptext(),
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

    return data


def rating_user_data(slug=None):
    data = {
        'user': {
            'has_rated': rand_bool(),
            'can_rate': True,
        }
    }
    if data['user']['can_rate']:
        data['rating'] = random.randint(1, 5)
        data['user']['has_rated'] = rand_bool()

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
            'developed': rand_bool(),
        }
    }
    # Conditional slugs for great debugging.
    if slug == 'developed':
        data['user']['developed'] = True
    elif slug == 'user':
        data['user']['developed'] = False

    return data


def app_user_review(slug, **kwargs):
    data = {
        'body': kwargs.get('review', ptext()),
        'rating': 4
    }
    return data


user_names = ['Cvan', 'Basta', 'Davor', 'Queen Krupa']


def rand_datetime():
    rand_date = datetime.now() - timedelta(days=random.randint(0, 600))
    return rand_date.strftime('%Y-%m-%dT%H:%M:%S')


def rating():
    version = None
    if random.choice((True, False)):
        version = {
            'name': random.randint(1, 3),
            'latest': False,
        }

    id_ = random.randint(1000, 9999)
    return {
        'rating': 4,
        'body': ptext(len=20),
        'created': rand_datetime(),
        'is_flagged': random.randint(1, 5) == 1,
        'is_author': random.randint(1, 5) == 1,
        'modified': rand_datetime(),
        'report_spam': '/api/v1/apps/rating/%d/flag/' % id_,
        'resource_uri': '/api/v1/apps/rating/%d/' % id_,
        'user': {
            'display_name': text(random.choice(user_names)),
            'id': random.randint(1000, 9999),
        },
        'version': version,
    }


def collection(name, slug, num=6):
    description = random.choice([ptext(len=20), ''])
    collection_id = random.randint(1, 999)

    rand_color = random.choice(COLLECTION_COLORS)

    data = {
        'name': text(name),
        'id': collection_id,
        'slug': slug,
        'app_count': num,
        'type': 'listing',
        'author': text('Basta Splasha'),
        'description': description,
        'apps': [app('Featured App', 'creat%d' % i) for
                 i in xrange(num)],
        'background_color': rand_color[1],
        'color': rand_color[0],
        'icon': 'http://f.cl.ly/items/103C0e0I1d1Q1f2o3K2B/'
                'mkt-collection-logo.png',
        'url': '/api/v2/feed/collections/%d/' % collection_id
    }

    if random.randint(0, 1):
        data['background_image'] = SAMPLE_BG_IMAGE,
        data['type'] = 'promo'
    return data


def region(**kwargs):
    return {
        'id': kwargs.get('id', 1),
        'name': kwargs.get('name', 'Appistan'),
        'resource_uri': kwargs.get('resource_uri',
                                   '/api/v1/services/region/ap/'),
        'slug': random.choice(REGIONS),
        'default_currency': kwargs.get('default_currency', 'USD'),
        'default_language': kwargs.get('default_language', 'en-AP'),
    }


def carrier(**kwargs):
    return {
        'id': kwargs.get('id', 1),
        'name': kwargs.get('name', 'Seavan Sellular'),
        'resource_uri': kwargs.get('resource_uri',
                                   '/api/v1/services/carrier/seavan_sellular/'),
        'slug': random.choice(CARRIERS),
    }


def feed_item(item_type=None):
    item_id = random.randint(1, 999)
    coll = collection('some feed collection',
                      'some_feed_collection_%d' % item_id,
                      num=random.randint(2, 5))

    return {
        'app': feed_app(),
        'brand': feed_brand(),
        'carrier': carrier()['slug'],
        'collection': coll,
        'id': item_id,
        'item_type': item_type or random.choice(['app', 'collection', 'brand']),
        'url': '/api/v2/feed/items/%d/' % item_id,
        'region': region()['slug'],
        'shelf': op_shelf()
    }


def feed_app():
    app_id = random.randint(1, 999)
    pq_text = '"' + ptext(len=12) + '"'
    description = random.choice([ptext(len=20), ''])
    feedapp_type = random.choice(FEED_APP_TYPES)

    rand_color = random.choice(COLLECTION_COLORS)

    return {
        'app': app('feed app %d' % app_id,
                   'feed-app-%d' % app_id, description=xss_text),
        'background_color': rand_color[1],
        'color': rand_color[0],
        'description': description,
        'type': feedapp_type,
        'background_image': SAMPLE_BG_IMAGE,
        'id': app_id,
        'preview': preview(),
        'pullquote_attribute': random.choice(AUTHORS),
        'pullquote_rating': random.randint(1, 5),
        'pullquote_text': pq_text,
        'slug': 'some-feed-app-%d' % app_id,
        'url': '/api/v2/feed/apps/%d' % app_id
    }


def feed_brand(num=6):
    bid = random.randint(1, 999)
    layout = random.choice(['list', 'grid'])

    # Full list at:
    # https://github.com/mozilla/zamboni/blob/master/mkt/feed/constants.py
    brand_type = random.choice(['hidden-gem', 'music', 'travel'])

    return {
        'apps': [app('Branded App', 'brand%d' % i) for
                 i in xrange(num)],
        'id': bid,
        'layout': layout,
        'slug': 'brand-%d' % bid,
        'type': brand_type,
        'url': '/api/v2/feed/brand%d' % bid
    }


def op_shelf(num=6):
    _carrier = carrier()['slug']
    shelf_id = random.randint(1, 999)

    data = {
        'apps': [app('Featured App', 'creat%d' % i) for
                 i in xrange(num)],
        'app_count': num,
        'background_image': SAMPLE_BG_IMAGE,
        'background_image_landing': SAMPLE_BG_IMAGE,
        'carrier': _carrier,
        'id': shelf_id,
        'name': '%s Op Shelf' % _carrier.replace('_', ' ').capitalize(),
        'region': 'restofworld',
        'slug': 'sample-op-shelf',
        'url': '/api/v2/feed/shelves/%d/' % shelf_id
    }

    if random.randint(0, 1):
        data['description'] = '<script>alert("LOL");</script> Description'

    return data


def preview():
    pid = random.randint(1, 999)

    return {
        'id': pid,
        'position': 1,
        'thumbnail_url': 'http://f.cl.ly/items/103C0e0I1d1Q1f2o3K2B/'
                         'mkt-collection-logo.png',
        'image_url': SAMPLE_BG_IMAGE,
        'filetype': 'image/png',
        'resource_uri': 'pi/v1/apps/preview/%d' % pid
    }
