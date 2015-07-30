from utils import text


AUTHORS = [
    text('Lord Basta of the Iron Isles'),
    text('Chris Van Halen'),
    text('Ngo Way'),
    text('Huck Charmston'),
    text('Davor van der Beergulpen')
]

CARRIERS = {
    'america_movil': 'America Movil',
    'kddi': 'Kddi',
    'o2': 'O2',
    'telefonica': 'Telefonica',
    'deutsche_telekom': 'DT',
}

REGIONS = {
    'de': 'Germany',
    'es': 'Spain',
    'mx': 'Mexico',
    'jp': 'Japan',
    'us': 'United States',
}

MESSAGES = [
    ['be careful, cvan made it', 'loljk'],
    ["it's probably a game or something"],
    None
]

PROMO_IMAGES = [
    'https://camo.githubusercontent.com/2b57d6cab55a353ad3527886d7c1d29e2fed4bda/687474703a2f2f66696c65732e6d6f6b612e636f2f73637265656e732f74616e785f30342e6a7067',
    'http://cdn.akamai.steamstatic.com/steam/apps/327310/header.jpg?t=1423847161',
    'http://8bitchimp.com/wp-content/uploads/2015/04/Bastion-2012-02-10-12-23-31-59.jpg',
    'https://lh3.ggpht.com/sobmPoqky8bnZZ14BZ87OusQPzD_c3BJM89E_hb1oUwACiT_s4C9WP2r5hC31C4IPzc=h900',
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
