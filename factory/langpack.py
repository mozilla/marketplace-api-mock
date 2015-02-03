# -*- coding: utf-8 -*-
import random
import uuid

from factory.utils import text


LANGUAGES = {
    'fr': u'Français',
    'it': u'Italiano',
    'de': u'Deutsch',
    'en-US': u'English (US)',
    'pt-BR': u'Português (do Brasil)',
    'pl': u'Polski'
}


def langpack(url_root):
    uuid_ = uuid.uuid4()
    language = random.choice(LANGUAGES.keys())
    return {
        'active': True,
        'name': '%s language pack for Firefox OS v2.2' % text(LANGUAGES[language]),
        'fxos_version': '2.2',
        'language': language,
        'language_display': text(LANGUAGES[language]),
        'manifest_url': '%s%s/manifest.webapp' % (url_root, unicode(uuid_)),
        'size': 666,
        'uuid': uuid_.hex,
        'version': '1.0.1'
    }
