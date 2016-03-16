# -*- coding: utf-8 -*-
from datetime import datetime
from django.db import models
from filer.models import Folder
from django.core.exceptions import ObjectDoesNotExist
from ..models import EventFile


def year_choices():
    year_choice = []

    for year in range(1980, (datetime.now().year+1)):
        year_choice.append((year, year))


class Ranks(models.Model):

    class Meta:
        verbose_name = "Rankingi weteranow"
        verbose_name_plural = "Rankingi weteranów"

    ranks_year = models.IntegerField("Rok rankingów", choices=year_choices())
    ranks_folder = models.ForeignKey(Folder)

    def save(self, *args, **kwargs):
        try:
            Folder.objects.get(name='Rankingi')
        except ObjectDoesNotExist:
            Folder(name='Rankingi', parent=None).save()
        try:
            self.ranks_folder
        except:
            parent_folder = Folder.objects.get(name='Rankingi')
            folder = Folder(name="Rankingi {rok}".format(rok=self.ranks_year), parent=parent_folder)
            folder.save()
            self.ranks_folder = folder

        super(Ranks, self).save(*args, **kwargs)

    @property
    def get_rank_files(self):
        event_files = []
        for fp in self.ranks_folder.files:
            event_files.append(EventFile.objects.get(id=fp.id))

        return event_files
