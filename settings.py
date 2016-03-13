#-*- coding: utf-8 -*-
from django.conf import settings
import os

gettext = lambda s: s
DATA_DIR = os.path.dirname(os.path.dirname(__file__))

ICON_SIZES = getattr(settings, "FILER_ADMIN_ICON_SIZES", (
    '16', '32', '64', '128'
    ))

FILER_FILE_MODELS = 'pzwla_events.models.DocumentFile'

SUPPORTED_EXTENSIONS = {
    'pdf': ['pdf'],
    'regular': ['doc', 'docx', 'odt'],
    'excel': ['xls', 'xlsx'],
    'image': ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'svg'],
    'audio': ['mp3', 'mp4', 'wav', 'ogg', 'aiff'],
    'video': ['avi'],
    'archive': ['zip', 'rar', 'tar.gz'],
    'text': ['txt']
}

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(DATA_DIR, 'media')
STATIC_ROOT = os.path.join(DATA_DIR, 'static')
