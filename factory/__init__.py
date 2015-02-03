import random
import string
from cgi import escape
from datetime import datetime, timedelta

from factory.constants import (AUTHORS, CARRIERS, MESSAGES, SPECIAL_APP_SLUGS,
                               REGIONS, SAMPLE_BG, SCREENSHOT_MAP,
                               SPECIAL_SLUGS_TO_IDS, USER_NAMES)
from factory.utils import rand_bool, rand_text, rand_datetime, text


counter = 0


def _app_preview():
    """Generate app preview object."""
    url = ('https://marketplace.cdn.mozilla.net/'
           'img/uploads/previews/%%s/%d/%d.png' %
           random.choice(SCREENSHOT_MAP))
    return {
        'caption': rand_text(n=5),
        'filetype': 'image/png',
        'thumbnail_url': url % 'thumbs',
        'image_url': url % 'full',
    }


def carrier(**kw):
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
        'name': text(name),
        'slug': slug,
    }


def region(**kw):
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
        'current_version': text('%d.0' % int(random.random() * 20)),
        'description': {'en-US': escape(kw.get('description',
                                               rand_text(100)))},
        'device_types': ['desktop', 'firefoxos', 'android-mobile',
                         'android-tablet'],
        'file_size': 12345,
        'homepage': 'http://marketplace.mozilla.org/',
        'icons': {
            64: '/media/img/logos/64.png'
        },
        'is_packaged': slug == 'packaged' or rand_bool(),
        'manifest_url':
            'http://%s%s.testmanifest.com/manifest.webapp' %
            (rand_text(1), random.randint(1, 50000)),  # Minifest if packaged
        'name': text('App %d' % counter),
        'notices': random.choice(MESSAGES),
        'previews': [_app_preview() for i in range(4)],
        'privacy_policy': kw.get('privacy_policy', rand_text()),
        'public_stats': False,
        'slug': slug,
        'ratings': {
            'average': random.random() * 4 + 1,
            'count': int(random.random() * 500),
        },
        'release_notes': kw.get('release_notes', rand_text(100)),
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
            'name': rand_text(),
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

    if slug in SPECIAL_APP_SLUGS:
        data['name'] = string.capwords(slug.replace('_', ' '))

    data.update(app_user_data(slug))

    return dict(data, **kw)


def review_user_data(slug=None):
    data = {
        'user': {
            'has_rated': False,
            'can_rate': True,
        }
    }
    if data['user']['can_rate']:
        data['rating'] = random.randint(1, 5)
        data['user']['has_rated'] = False

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


def app_user_review(slug, **kw):
    data = {
        'body': kw.get('review', rand_text()),
        'rating': 4
    }
    return data


def review(**kw):
    global counter
    counter += 1

    version = None
    if rand_bool():
        version = {
            'name': random.randint(1, 3),
            'latest': False,
        }

    return dict({
        'rating': random.randint(1, 5),
        'body': rand_text(n=20),
        'created': rand_datetime(),
        'is_flagged': False,
        'is_author': False,
        'modified': rand_datetime(),
        'report_spam': '/api/v1/apps/rating/%d/flag/' % counter,
        'resource_uri': '/api/v1/apps/rating/%d/' % counter,
        'user': {
            'display_name': text(random.choice(USER_NAMES)),
            'id': counter,
        },
        'version': version,
    }, **kw)


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
