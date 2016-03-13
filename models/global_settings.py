#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime


class EventsGlobalSettings(models.Model):

    class Meta:
        verbose_name = "Ustawienia globalne zawodów"
        verbose_name_plural = "Ustawienia globalne zawodów"

    calendar_year = models.IntegerField("rok kalendarza", max_length=4, choices=year_choices(),
                                        default=datetime.now().year)
    results_year = models.IntegerField("rok wyników", max_length=4, choices=year_choices(), default=datetime.now().year)

    def __unicode__(self):
        return u"Rok kalendarza: {rok_kalendarz}, Rok wyników: {rok_wyniki}".format(rok_kalendarz=self.calendar_year,
                                                                                    rok_wyniki=self.results_year)


def year_choices():
    year_choice = []

    for year in range(1980, (datetime.now().year+1)):
        year_choice.append((year, year))
