import random
import string
from cgi import escape
from uuid import uuid4

from factory.constants import (AUTHORS, CARRIERS, MESSAGES, PROMO_IMAGES,
                               SPECIAL_APP_SLUGS, REGIONS, SAMPLE_BG,
                               SCREENSHOT_MAP, SPECIAL_SLUGS_TO_IDS,
                               USER_NAMES)
from factory.utils import rand_bool, rand_text, rand_datetime, text


counter = 0
extension_counter = 0
preview_counter = 0
review_counter = 0
website_counter = 0

CDN_URL = 'https://marketplace-dev-cdn.allizom.org'


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
    slug = kw.get('slug')
    if not slug:
        # No slug ? Pick a random carrier from the dict.
        slug, name = random.choice(CARRIERS.items())
    else:
        # A slug was given ? Pick the corresponding carrier name or just make
        # one up.
        name = CARRIERS.get(slug, 'Seavan Sellular')
    return {
        'id': kw.get('id', 1),
        'name': name,
        'slug': slug,
    }


def _category(slug, name):
    """Creates a category object."""
    return {
        'name': text(name),
        'slug': slug,
    }


def region(**kw):
    slug = kw.get('slug')
    if not slug:
        # No slug ? Pick a random region from the dict.
        slug, name = random.choice(REGIONS.items())
    else:
        # A slug was given ? Pick the corresponding region name or just make
        # one up.
        name = REGIONS.get(slug, 'Cvanistan')
    return {
        'id': kw.get('id', 1),
        'name': name,
        'slug': slug,
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

    num_previews = kw.get('num_previews', 4)
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
                         'android-tablet', 'firefoxos-tv'],
        'file_size': 12345,
        'homepage': 'http://marketplace.mozilla.org/',
        'icons': {
            64: '/media/img/logos/64.png'
        },
        'is_packaged': slug == 'packaged' or rand_bool(),
        'last_updated': rand_datetime(),
        'manifest_url':
            # Minifest if packaged
            'http://%s.testmanifest.com/manifest.webapp' % slug,
        'name': text('App %d' % counter),
        'notices': random.choice(MESSAGES),
        'premium_type': 'free',
        'previews': [_app_preview() for i in range(num_previews)],
        'price': None,
        'price_locale': '$0.00',
        'promo_images': {
            'small': random.choice(PROMO_IMAGES),
            'large': random.choice(PROMO_IMAGES),
        },
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
        'tv_featured': random.choice([True, False]),
        'upsell': False,
    }

    data.update(app_user_data(slug))
    data = dict(data, **kw)

    # Special apps.
    if slug == 'paid':
        data.update(
            price=3.50,
            price_locale='$3.50',
            payment_required=True
        )
    elif slug == 'upsell':
        data['upsell'] = {
            'id': random.randint(1, 10000),
            'name': rand_text(),
            'icon_url': '/media/img/logos/firefox-256.png',
            'app_slug': 'upsold',
            'resource_uri': '/api/v1/fireplace/app/%s/' % 'upsold',
        }
    elif slug == 'packaged':
        data['current_version'] = '1.0'
    elif slug == 'unrated':
        data['ratings'] = {
            'average': 0,
            'count': 0,
        }
    elif slug == 'tracking':
        data['id'] = 1234
        data['author'] = 'Tracking'
        data['name'] = 'Tracking'
    elif slug.startswith('num-previews-'):
        data['previews'] = [_app_preview() for x in
                            range(int(slug.split('num-previews-')[1]))]

    if slug in SPECIAL_APP_SLUGS or slug.startswith('num-previews-'):
        data['name'] = string.capwords(
            slug.replace('_', ' ').replace('-', ' '))

    return data


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


def review(slug=None, **kw):
    global review_counter
    review_counter += 1

    version = None
    if rand_bool():
        version = {
            'name': random.randint(1, 3),
            'latest': False,
        }

    data = dict({
        'rating': random.randint(1, 5),
        'body': rand_text(n=20),
        'created': rand_datetime(),
        'has_flagged': False,
        'is_author': False,
        'modified': rand_datetime(),
        'report_spam': '/api/v1/apps/rating/%d/flag/' % review_counter,
        'resource_uri': '/api/v1/apps/rating/%d/' % review_counter,
        'user': {
            'display_name': text(random.choice(USER_NAMES)),
            'id': review_counter,
        },
        'version': version,
    }, **kw)

    if slug == 'has_flagged':
        data['has_flagged'] = True

    return data


def preview():
    global preview_counter
    preview_counter += 1

    return {
        'id': preview_counter,
        'position': 1,
        'thumbnail_url': 'http://f.cl.ly/items/103C0e0I1d1Q1f2o3K2B/'
                         'mkt-collection-logo.png',
        'image_url': SAMPLE_BG,
        'filetype': 'image/png',
        'resource_uri': 'pi/v1/apps/preview/%d' % preview_counter
    }


def extension(**kw):
    global extension_counter
    extension_counter += 1
    slug = kw.get('slug', 'add-on-%d' % extension_counter)
    uuid = unicode(uuid4()).replace('-', '')

    data = {
        'id': SPECIAL_SLUGS_TO_IDS.get(slug, extension_counter),
        'author': random.choice(AUTHORS),
        'description': {
            'en-US': escape(kw.get('description', rand_text(20))),
        },
        'device_types': [
            'firefoxos'
        ],
        'disabled': False,
        'icons': {
            '64': '%s/media/img/mkt/logos/64.png' % CDN_URL,
            '128': '%s/media/img/mkt/logos/128.png' % CDN_URL,
        },
        'last_updated': '2015-10-30T15:50:40',
        'latest_public_version': {
            'id': 294,
            'created': '2015-10-29T13:53:12',
            'download_url': '/extension/%s/42/extension-0.1.zip' % uuid,
            'reviewer_mini_manifest_url':
                '/extension/reviewers/%s/42/manifest.json' % uuid,
            'unsigned_download_url':
                '/downloads/extension/unsigned/%s/42/extension-0.1.zip' % uuid,
            'size': 19062,
            'status': 'public',
            'version': '0.1'
        },
        'mini_manifest_url': '/extension/%s/manifest.json' % uuid,
        'name': {
            'en-US': text('Add-on %d' % extension_counter),
        },
        'slug': slug,
        'status': 'public',
        'uuid': uuid,
    }
    data = dict(data, **kw)
    return data


def website(**kw):
    global website_counter
    website_counter += 1

    domain = '%s.example.com' % rand_text(2, separator='')
    data = {
        'categories': [
            'news-weather'
        ],
        'description': {
            'en-US': escape(kw.get('description', rand_text(30))),
        },
        'device_types': [
            'firefoxos'
        ],
        'icons': {
            '64': '%s/media/img/mkt/logos/64.png' % CDN_URL,
            '128': '%s/media/img/mkt/logos/128.png' % CDN_URL,
        },
        'id': website_counter,
        'mobile_url': 'http://m.%s/' % domain,
        'name': {
            'en-US': text('Website %d' % website_counter),
        },
        'short_name': {
            'en-US': text('Site %d' % website_counter),
        },
        'title': {
            'en-US': text('Website Title %d' % website_counter),
        },
        'url': 'http://%s/' % domain
    }
    data = dict(data, **kw)
    return data
