# -*- coding: utf-8 -*-
from django.db import models
from filer.models import Folder
from ..models import EventFile


class Statistics(models.Model):

    class Meta:
        verbose_name = "Statystyki"
        verbose_name_plural = "Statystyki"

    name = models.CharField("Statystyki", max_length=20, default='Statystyki')
    folder = models.ForeignKey(Folder)

    def save(self, *args, **kwargs):
        folder = Folder(name="Statystki", parent=None)
        folder.save()
        self.folder = folder

        super(Statistics, self).save(*args, **kwargs)

    @property
    def get_records_files(self):
        stats_files = []
        for fp in self.folder.files:
            stats_files.append(EventFile.objects.get(id=fp.id))

        return stats_files
