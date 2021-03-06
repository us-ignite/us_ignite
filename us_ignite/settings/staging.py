# Staging environment settings for us_ignite
import datetime
import os
import urlparse

from us_ignite.settings.base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Sensitive values are saved as env variables:
env = os.getenv
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
# settings is one directory up now
here = lambda *x: os.path.join(PROJECT_ROOT, '..', *x)

SITE_URL = 'https://us-ignite-staging.herokuapp.com'

ALLOWED_HOSTS = [
    'us-ignite-staging.herokuapp.com',
]

# HTTPS configuration:
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 60 * 5
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = env('SECRET_KEY')


# Remote storage settings:
STATICFILES_STORAGE = 'us_ignite.common.storage.StaticS3Storage'
DEFAULT_FILE_STORAGE = 'us_ignite.common.storage.MediaS3Storage'
THUMBNAIL_DEFAULT_STORAGE = DEFAULT_FILE_STORAGE

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')

AWS_STORAGE_BUCKET_NAME = 'staging-us-ignite-org'

expire_date = datetime.date.today() + datetime.timedelta(days=365)
expire_seconds = 30 * 24 * 60 * 60
AWS_HEADERS = {
    'Expires': expire_date.strftime('%a, %d %b %Y 00:00:00 GMT'),
    'Cache-Control': 'max-age=%s' % expire_seconds,
}

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = 'https://%s/static/' % AWS_S3_CUSTOM_DOMAIN

redis_url = urlparse.urlparse(env('REDISTOGO_URL'))

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': '%s:%s' % (redis_url.hostname, redis_url.port),
        'OPTIONS': {
            'DB': 0,
            'PASSWORD': redis_url.password,
        }
    }
}

# Email:
EMAIL_SUBJECT_PREFIX = '[STAGE US Ignite] '
DEFAULT_FROM_EMAIL = 'info@staging.us-ignite.org'
SERVER_EMAIL = 'info@staging.us-ignite.org'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')


# Twitter API:
TWITTER_API_KEY = env('TWITTER_API_KEY')
TWITTER_API_SECRET = env('TWITTER_API_SECRET')

# WP email
WP_EMAIL = env('WP_EMAIL')


# Enable dummy content generation on this build:
ENABLE_DUMMY = True
if ENABLE_DUMMY:
    INSTALLED_APPS += ('us_ignite.dummy', )
    # List of words:
    WORDS_PATH = here('..', 'words')


MAILCHIMP_API_KEY = env('MAILCHIMP_API_KEY')
MAILCHIMP_LIST = env('MAILCHIMP_LIST')

GOOGLE_ANALYTICS_ID = 'DUMMY'

# Production flag:
IS_PRODUCTION = True

# Asset compressor:
COMPRESS_ENABLED = True
STATIC_FILES_VERSION = 'v1'
# Heroku does not have a filesystem, used to deploy the assets to S3:
COMPRESS_STORAGE = 'us_ignite.common.storage.CachedS3BotoStorage'

USE_DEBUG_TOOLBAR = False