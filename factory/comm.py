from factory import app


counter = 0


def thread(**kw):
    global counter
    counter += 1

    return {
        'app': app(),
        'id': counter,
        'notes_count': 5,
        'version': {
            'deleted': False,
            'id': 45,
            'version': '1.6'
        }
    }


def note(**kw):
    return {
        'attachments': [{
            'id': 1,
            'created': '2013-06-14T11:54:48',
            'display_name': 'Screenshot of my app.',
            'url': 'http://marketplace.cdn.mozilla.net/someImage.jpg',
        }],
        'author': 1,
        'author_meta': {
            'name': 'Admin'
        },
        'body': 'hi there',
        'created': '2013-06-14T11:54:48',
        'id': 2,
        'note_type': 0,
        'thread': 2,
    }
