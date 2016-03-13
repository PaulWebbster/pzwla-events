#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.core.validators import RegexValidator


class Organizer(models.Model):

    class Meta:
        verbose_name = "Organizator"
        verbose_name_plural = "Organizatorzy"

    name = models.CharField("Nazwa organizatora", max_length=300)
    street = models.CharField("Ulica", max_length=300)
    postal_code = models.CharField("Kod pocztowy", max_length=10, blank=True)
    city = models.CharField("Miasto", max_length=100)
    country = models.CharField("Kraj", max_length=100)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Numer telefonu musi byc w następującym formacie: "
                                                                   "'+999999999'. Maksymalna liczba cyfr to 15.")
    phone_number = models.CharField("Telefon", validators=[phone_regex], blank=True, max_length=16)
    fax_number = models.CharField("Fax", validators=[phone_regex], blank=True, max_length=16)

    def __unicode__(self):
        return u"%s" % self.name
