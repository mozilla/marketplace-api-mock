import random
from cgi import escape
from datetime import date, timedelta


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
    text('basta'),
    text('cvan'),
    text('Chris Van Halen')
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

COLLECTION_COLORS = [
    '#00953f',
    '#f78813',
    '#ce001c',
    '#a20d55',
    '#5a197e',
    '#1e1e9c',
    '#0099d0',
]

FEED_APP_TYPES = [
    'icon',
    'image',
    'description',
    'quote',
    'preview'
]

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
        'name': text(name),
        'slug': slug,
        'description': {'en-US': escape(kwargs.get('description',
                                                   ptext(100)))},
        'is_packaged': slug == 'packaged' or rand_bool(),
        'manifest_url':
            'http://%s%s.testmanifest.com/manifest.webapp' %
            (ptext(1), random.randint(1, 50000)),  # Minifest if packaged
        'current_version': text('%d.0' % int(random.random() * 20)),
        'icons': {
            64: 'https://marketplace.cdn.mozilla.net/img/uploads/addon_icons/461/461685-64.png',
        },
        'previews': [_app_preview() for i in range(4)],
        'author': random.choice(AUTHORS),
        'ratings': {
            'average': random.random() * 4 + 1,
            'count': int(random.random() * 500),
        },
        'release_notes': kwargs.get('release_notes', ptext(100)),
        'notices': random.choice(MESSAGES),
        'support_email': text('support@%s.com' % slug),
        'homepage': 'http://marketplace.mozilla.org/',
        'privacy_policy': kwargs.get('privacy_policy', ptext()),
        'public_stats': False,
        'upsell': False,
        'content_ratings': {
            'body': 'generic',
            'rating': '12',
            'descriptors': ['scary', 'lang', 'drugs'],
            'interactives': ['users-interact', 'shares-info']
        },
        'device_types': ['desktop', 'firefoxos', 'android-mobile',
                         'android-tablet'],
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
            'can_rate': rand_bool(),
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


def rand_posted():
    rand_date = date.today() - timedelta(days=random.randint(0, 600))
    return rand_date.strftime('%b %d %Y %H:%M:%S')


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
        'is_flagged': random.randint(1, 5) == 1,
        'is_author': random.randint(1, 5) == 1,
        'posted': rand_posted(),
        'report_spam': '/api/v1/apps/rating/%d/flag/' % id_,
        'resource_uri': '/api/v1/apps/rating/%d/' % id_,
        'user': {
            'display_name': text(random.choice(user_names)),
            'id': random.randint(1000, 9999),
        },
        'version': version,
    }


def collection(name, slug, num=3, **kwargs):
    ctype = random.choice(['collection', 'shelf'])
    cname = name
    description = random.choice([ptext(len=20), ''])

    if ctype == 'shelf':
        cname = 'some operator shelf'

    return {
        'name': text(cname),
        'slug': slug,
        'collection_type': ctype,
        'author': text('Basta Splasha'),
        'description': description,
        'apps': [app('Featured App', 'creat%d' % i) for
                 i in xrange(num)],
        'background_color': COLLECTION_COLORS[random.randint(0, 6)],
        'background_image': '/media/img/sample_bg.jpg',
        'icon': 'http://f.cl.ly/items/103C0e0I1d1Q1f2o3K2B/'
                'mkt-collection-logo.png'
    }


def region(**kwargs):
    return {
        'id': kwargs.get('id') or 1,
        'name': kwargs.get('name') or 'Appistan',
        'resource_uri': kwargs.get('resource_uri') or
                        '/api/v1/services/region/ap/',
        'slug': kwargs.get('slug') or 'ap',
        'default_currency': kwargs.get('default_currency') or 'USD',
        'default_language': kwargs.get('default_language') or 'en-AP',
    }


def carrier(**kwargs):
    return {
        'id': kwargs.get('id') or 1,
        'name': kwargs.get('name') or 'Seavan Sellular',
        'resource_uri': kwargs.get('resource_uri') or
                        '/api/v1/services/carrier/seavan_sellular/',
        'slug': kwargs.get('slug') or 'seavan_selluar',
    }


def feed_item(item_type='collection'):
    item_id = random.randint(1, 999)
    coll=collection('some feed collection',
                    'some_feed_collection_%d' % item_id,
                    num=random.randint(2, 5))

    return {
        'app': feed_app(),
        'carrier': carrier()['slug'],
        'collection': coll,
        'id': item_id,
        'item_type': item_type,
        'resource_url': '/api/v2/feed/items/%d/' % item_id,
        'region': region()['slug']
    }


def feed_app():
    app_id = random.randint(1, 999)
    pullquote = ptext(len=10)
    pq_text = '"' + ptext(len=12) + '"'
    description = random.choice([ptext(len=20), ''])
    feedapp_type = random.choice(FEED_APP_TYPES)

    return {
        'app': app('feed app %d' % app_id, 'feed-app-%d' % app_id, description=xss_text),
        'background_color': COLLECTION_COLORS[random.randint(0, 6)],
        'description': description,
        'feedapp_type': feedapp_type,
        'background_image': '/media/img/sample_bg.jpg',
        'id': app_id,
        'preview': preview(),
        'pullquote_attribute': 'Kevin Ngo',
        'pullquote_rating': random.randint(1, 5),
        'pullquote_text': pq_text,
        'slug': 'some-feed-app-%d' % app_id,
        'url': '/api/v2/feed/apps/%d' % app_id
    }


def preview():
    pid = random.randint(1, 999)

    return {
        'id': pid,
        'position': 1,
        'thumbnail_url': 'http://f.cl.ly/items/103C0e0I1d1Q1f2o3K2B/'
                         'mkt-collection-logo.png',
        'image_url': '/media/img/sample_bg.jpg',
        'filetype': 'image/png',
        'resource_uri': 'pi/v1/apps/preview/%d' % pid
    }
