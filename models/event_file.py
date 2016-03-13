#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from filer.models import File
from ..settings import *
from django.contrib.staticfiles.templatetags.staticfiles import static


class EventFile(File):
    class Meta:
        proxy = True

    objects = models.Manager()

    @classmethod
    def matches_file_type(cls, iname, ifile, request):
        # the extensions we'll recognise for this file type
        filename_extensions = ['.doc', '.docx', '.pdf', '.xls', '.odt', ]
        ext = os.path.splitext(iname)[1].lower()
        return ext in filename_extensions

    @property
    def get_document_icon(self):
        r = {}
        ext = os.path.splitext(str(self.file))[1][1:]
        file_img = 'regular'
        for extension in SUPPORTED_EXTENSIONS:
            if ext in SUPPORTED_EXTENSIONS[extension]:
                file_img = extension

        for size in ICON_SIZES:
            r[size] = static('pzwla_events/icons/%s_file_%sx%s.png' % (file_img, size, size))
        return r['32']

    @property
    def get_mb_size(self):
        return "%.2f MB" % (float(self.size)/1024/1024)
