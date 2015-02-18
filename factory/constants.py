from utils import text


AUTHORS = [
    text('Lord Basta of the Iron Isles'),
    text('Chris Van Halen'),
    text('Ngo Way'),
    text('Huck Charmston'),
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

SAMPLE_BG = '/media/img/logos/firefox-256.png'

# App slugs that return special data.
SPECIAL_APP_SLUGS = [
    'can_rate',
    'cant_rate',
    'developed',
    'has_rated',
    'packaged',
    'paid',
    'unrated',
    'upsell',
]

# Mapping between special app slug to their ids.
SPECIAL_SLUGS_TO_IDS = {
    'free': 1,
    'installed': 414141,
    'developed': 424242,
    'purchased': 434343,
}

USER_NAMES = ['Von Cvan', 'Lord Basta', 'Ser Davor', 'Queen Krupa',
              'Le Ngoke']
