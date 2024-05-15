import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'movies_database',
        'USER': 'app',
        'PASSWORD': '123qwe',
        'HOST': 'database',
        'PORT': '5432',
        'OPTIONS': {
            'options': '-c search_path=public,content'
        }
    }
} 

