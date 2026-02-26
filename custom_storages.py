from django.conf import settings
from storages.backends.s3boto3 import S3Botot3Storage

class StaticFileStorage(S3Botot3Storage):
    location = settings.STATICFILES_FOLDER

class MediaFileStorage(S3Botot3Storage):
    location = settings.MEDIAFILES_FOLDER