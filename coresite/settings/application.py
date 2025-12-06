DJANGO_APPLICATIONS = [
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
    "channels",

]

CUSTOM_APPLICATIONS = [
    'apps.core',
    'apps.userprofile',
    "apps.restaurants",
    "apps.super_admin",
    'apps.owner',
    'apps.dashboard',

]

THIRD_PARTY_APPLICATIONS = [

    'corsheaders',
    'drf_yasg',
    'rest_framework',
]
