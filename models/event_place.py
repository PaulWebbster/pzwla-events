#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models


class EventPlace(models.Model):

    class Meta:
        verbose_name = "Miejsce zawodów"
        verbose_name_plural = "Miejsca zawodów"

    city = models.CharField("Miasto", max_length=100)
    country = models.CharField("Kraj", max_length=100)
    stadium = models.CharField("Stadion", max_length=100, blank=True)

    def __unicode__(self):
        return u"%s in %s (%s)" % (self.stadium, self.city, self.country)
