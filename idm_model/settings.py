SECRET_KEY = 'very secret indeed'

INSTALLED_APPS = [
    'idm_model',
    'django_extensions',
    'django.contrib.contenttypes',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            # ... some options here ...
        },
    },
]
