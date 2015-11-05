from datetime import datetime, timedelta
import random


XSS = False


xss_text = '"\'><script>alert("poop");</script><\'"'


def text(default):
    return xss_text if XSS else default


dummy_text = ('foo bar zip zap cvan fizz buzz something martian salad '
              'potato quality space ship rotfl alfalfa platypus dinosaur '
              'shark bear dog cat snake elephant enough of this').split()


def rand_text(n=10, separator=' '):
    """Generate random string."""
    return text(separator.join(random.choice(dummy_text) for i in xrange(n)))


def rand_bool():
    """Randomly returns True or False."""
    return bool(random.getrandbits(1))


def rand_datetime():
    """Randomly returns a datetime within the last 600 days."""
    rand_date = datetime.now() - timedelta(days=random.randint(0, 600))
    return rand_date.strftime('%Y-%m-%dT%H:%M:%S')
