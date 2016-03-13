#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from geoposition.fields import GeopositionField
from datetime import datetime
from django.utils.text import slugify
import pytz
from filer.models import Folder
from event_place import EventPlace
from organizer import Organizer
from event_file import EventFile

utc = pytz.UTC


class FieldEvent(models.Model):

    class Meta:
        verbose_name = "Zawody"
        verbose_name_plural = "Zawody"

    name = models.CharField("Nazwa zawodów", max_length=300)
    short_name = models.CharField("Skrócona nazwa zawodów", max_length=50,
                                  help_text="Skrócona nazwa zawodów wyświetlana w menu oraz alternatywnie w przypadku "
                                  "braku loga na stronie informacyjnej zawodów. (Maximum 50 znaków)")
    slug = models.SlugField(max_length=50, editable=False)
    in_calendar = models.BooleanField("Dodać do kalendarza zawodów?")
    place = models.ForeignKey(EventPlace, verbose_name="Miejsce zawodów")
    date_time = models.DateTimeField("Data/godzina rozpoczęcia zawodów")
    end_date_time = models.DateTimeField("Data/godzina zakończenia zawodów", blank=True,
                                         help_text="Opcjonalne pole do uzupełnienia gdy zawody są dłuższe niż jeden "
                                                   "dzień")
    logo = models.ImageField("Logo zawodów", blank=True)
    site = models.CharField("Strona zawodów", max_length=300, blank=True)
    email = models.EmailField("e-mail", blank=True)
    entries = models.CharField("Zapisy - link do strony z zapisami", max_length=300, blank=True)
    results = models.CharField("Wyniki - link do strony z wynikami", max_length=300, blank=True)
    results_file = models.FileField("Plik z wynikami", blank=True, help_text="Jeżeli zamieszczony zostanie plik z "
                                                                             "wynikami to będzie on wyświetlany na "
                                                                             "stronie w zastępstwie linku do wyników na"
                                                                             " stronie organizatora/zawodów.")
    timetable = models.CharField("Harmonogram - link do strony z harmonogramem", max_length=300, blank=True)
    timetable_file = models.FileField("Plik z Harmonogramem", blank=True, help_text="Jeżeli zamieszczony zostanie plik "
                                                                                    "z harmonogramem to będzie on"
                                                                                    " wyświetlany w zastępstwie linku "
                                                                                    "do harmonogramu na stronie "
                                                                                    "organizatora/zawodów.")
    entry_booklet = models.CharField("Komunikat techniczny - link do strony z komunikatem", max_length=300, blank=True)
    entry_booklet_file = models.FileField("Plik z komunikatem technicznym", blank=True,
                                          help_text="Jeżeli zostanie zamieszczony plik z komunikatem technicznym to "
                                                    "będzie on wyświetlany w zastępstwie linku do komunikatu "
                                                    "technicznego na stronie organizatora/zawodów.")
    team_file = models.FileField("Kadra", blank=True, help_text="W tym polu można umieścić plik pdf z listą zawodników"
                                                                "kadry narodowej startujących w zawodach "
                                                                "międzynarodowych")
    organizer = models.ForeignKey(Organizer, blank=True, verbose_name="Organizator")
    preferable = models.BooleanField("Wyróżniony", default=False, help_text="Jeżeli zawody są oznaczone jako wyróżnione"
                                                                            " to wyświetlane są zawsze jako wydarzenia "
                                                                            "nadchodzące.")
    position = GeopositionField()
    event_folder = models.ForeignKey(Folder)

    def save(self, *args, **kwargs):
        if not self.end_date_time:
            self.end_date_time = self.date_time

        try:
            self.event_folder
        except:
            folder = Folder(parent=Folder.objects.all().filter(id=1)[0], name=self.short_name)
            folder.save()
            self.event_folder = folder

        if not self.id:
            self.slug = slugify(unicode(self.short_name))

        super(FieldEvent, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"Zawody: {nazwa}".format(nazwa=self.name)

    def date_from_past(self):
        now = datetime.now().replace(tzinfo=utc)
        event_date = self.date_time.replace(tzinfo=utc)
        if now > event_date:
            return True
        return False

    is_from_past = property(date_from_past)

    @property
    def get_event_files(self):
        event_files = []
        for fp in self.event_folder.files:
            event_files.append(EventFile.objects.get(id=fp.id))

        return event_files
