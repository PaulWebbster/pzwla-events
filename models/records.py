# -*- coding: utf-8 -*-
from django.db import models
from filer.models import Folder
from ..models import EventFile


class Records(models.Model):

    class Meta:
        verbose_name = "Rekordy"
        verbose_name_plural = "Rekordy"

    name = models.CharField("Rekordy", max_length=20, default='Rekordy')
    folder = models.ForeignKey(Folder)

    def save(self, *args, **kwargs):
        folder = Folder(name="Rekordy", parent=None)
        folder.save()
        self.folder = folder

        super(Records, self).save(*args, **kwargs)

    @property
    def get_records_files(self):
        records_files = []
        for fp in self.folder.files:
            records_files.append(EventFile.objects.get(id=fp.id))

        return records_files
