from project.settings import *

DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'cs542project',
            'USER': 'mludwig',
            'PASSWORD': 'pass',
            'HOST': '127.0.0.1',
            'PORT': '3306'
    }
}
