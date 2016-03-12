#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.validators import RegexValidator
from django.db import models
from geoposition.fields import GeopositionField
from cms.models import CMSPlugin
from datetime import datetime
from django.utils.timezone import make_aware
from django.utils import timezone
import pytz
from filer.models import Folder

utc = pytz.UTC


class EventPlace(models.Model):

    class Meta:
        verbose_name = "Miejsce zawodów"
        verbose_name_plural = "Miejsca zawodów"

    city = models.CharField("Miasto", max_length=100)
    country = models.CharField("Kraj", max_length=100)
    stadium = models.CharField("Stadion", max_length=100, blank=True)

    def __unicode__(self):
        return u"%s in %s (%s)" % (self.stadium, self.city, self.country)


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


class EventCategory(models.Model):

    class Meta:
        verbose_name = "Kategoria zawodów"
        verbose_name_plural = "Kategorie zawodów"

    name = models.CharField("Nazwa kategorii", max_length=300)

    def name_to_acronym(self):
        acronym = self.name.replace(" ", "_").lower()
        acronym = acronym.replace(
            u"ą", "a").replace(
            u"ę", "e").replace(
            u"ć", "c").replace(
            u"ł", "l").replace(
            u"ń", "n").replace(
            u"ó", "o").replace(
            u"ś", "s").replace(
            u"ź", "z").replace(
            u"ż", "z")

        return acronym

    acronym = property(name_to_acronym)

    def __unicode__(self):
        return u"%s" % self.name


class FieldEvent(models.Model):

    class Meta:
        verbose_name = "Zawody"
        verbose_name_plural = "Zawody"

    name = models.CharField("Nazwa zawodów", max_length=300)
    short_name = models.CharField("Skrócona nazwa zawodów", max_length=50, blank=True,
                                  help_text="Skrócona nazwa zawodów wyświetlana w menu oraz alternatywnie w przypadku "
                                  "braku loga na stronie informacyjnej zawodów. (Maximum 50 znaków)")
    acronym_regex = RegexValidator(regex=r'^[A-Z]{4,11}\d{4}[A-Z]{2,3}$')
    acronym = models.CharField("Akronim", validators=[acronym_regex], unique=True, max_length=18, help_text="Unikalny "
                               "akronim opisujący zawody. Używany przez stronę do nawigacji. Akronim powinien składać "
                               "się z od 4-11 liter oznaczających miejsce zawodów, 4 cyfr oznaczających rok oraz 2-3 "
                               "opisujących rangę zawodów. Przykład Halowe Mistrzostwa Polski w Toruniu w roku 2016 "
                               "można opisać jako TORUN2015HMP.")
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
    event_category = models.ManyToManyField(EventCategory)
    preferable = models.BooleanField("Wyróżniony", default=False, help_text="Jeżeli zawody są oznaczone jako wyróżnione"
                                                                            " to wyświetlane są zawsze jako wydarzenia "
                                                                            "nadchodzące.")
    position = GeopositionField()
    event_folder = models.ForeignKey(Folder)

    def save(self, *args, **kwargs):
        if not self.end_date_time:
            self.end_date_time = self.date_time
        if not self.event_folder:
            folder = Folder(parent=Folder.objects.all().filter(id=47)[0], name=self.short_name)
            folder.save()
            self.event_folder = folder
        super(FieldEvent, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"Zawody: {nazwa}, Akronim: {akronim}".format(nazwa=self.name, akronim=self.acronym)

    def date_from_past(self):
        now = datetime.now().replace(tzinfo=utc)
        event_date = self.date_time.replace(tzinfo=utc)
        if now > event_date:
            return True
        return False

    is_from_past = property(date_from_past)


def year_choices():
    year_choice = []

    for year in range(1980, (datetime.now().year+1)):
        year_choice.append((year, year))


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


