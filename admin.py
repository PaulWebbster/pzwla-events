# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.
from models import FieldEvent
from models import EventPlace
from models import Organizer
from models import EventsGlobalSettings
from models import Ranks
from models import Records
from models import Statistics
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html


class EventYearListFilter(admin.SimpleListFilter):
    title = _('rok zawodow')

    parameter_name = 'event_year'

    def lookups(self, request, model_admin):
        pass


class FieldEventAdmin(admin.ModelAdmin):
    list_display = ('event_date', "name", "place_city", "add_files_folder")
    list_display_links = ("name",)
    list_filter = ('date_time',)
    ordering = ('-date_time',)
    fieldsets = [
        ("Informacje podstawowe - Pola wymagane", {
            'classes': ('extrapretty',),
            'fields': ['name', 'short_name', 'place', 'organizer', 'preferable', 'in_calendar']}),
        ("Data zawodów - Pola wymagane", {
            'classes': ('collapse',),
            'fields': ['date_time', 'end_date_time']}),
        ("Kontak z organizatorem (e-mail, strona www zawodów)- Pola opcjonalne", {
            'classes': ('collapse',),
            'fields': ['email', 'site', 'logo']}),
        ("Informacje o zawodach (zapisy, wyniki, komunikat techniczny, itd.) - Pola opcjonalne", {
            'classes': ('collapse',),
            'fields': ['entries', 'entries_file', 'results', 'results_file', 'timetable', 'timetable_file', 'entry_booklet',
                       'entry_booklet_file', 'team_file']}),
        ("Mapka - wskazówki dojazdu na miejsce zawodów", {
            'classes': ('collapse',),
            'fields': ['position']
        }
         ),
    ]

    def event_date(self, obj):
        return obj.date_time.strftime("%d-%m-%Y")

    event_date.short_description = "Data zawodów"

    def add_files_folder(self, obj):
        return format_html('<a href="/admin/filer/folder/%s/list/">Dodaj pliki</a>' % obj.event_folder.id)
        show_firm_url.allow_tags = True

    add_files_folder.short_description = "Pliki"

    def place_city(self, obj):
        return obj.place.city

    place_city.short_description = "Miasto"


class RanksAdmin(admin.ModelAdmin):
    list_display = ('ranks_year', 'add_files_folder')

    def add_files_folder(self, obj):
        return format_html('<a href="/admin/filer/folder/%s/list/">Dodaj rankingi</a>' % obj.ranks_folder.id)
        show_firm_url.allow_tags = True

    add_files_folder.short_description = "Pliki"
    fields = ('ranks_year',)


class EventPlaceAdmin(admin.ModelAdmin):
    pass


class OrganizerAdmin(admin.ModelAdmin):
    pass


class EventsGlobalSettingsAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        # if there's already an entry, do not allow adding
        count = EventsGlobalSettings.objects.all().count()
        if count == 0:
            return True

        return False


class RecordsAdmin(admin.ModelAdmin):
    list_display = ('name', 'add_files_folder',)

    def add_files_folder(self, obj):
        return format_html('<a href="/admin/filer/folder/%s/list/">Dodaj/modyfikuj rekordy</a>' % obj.folder.id)
        show_firm_url.allow_tags = True

    add_files_folder.short_description = "Pliki rekordów"
    fields = ('name',)

    def has_add_permission(self, request):
        if Records.objects.all().count() == 0:
            return True

        return False


class StatisticsAdmin(admin.ModelAdmin):
    list_display = ('name', 'add_files_folder',)

    def add_files_folder(self, obj):
        return format_html('<a href="/admin/filer/folder/%s/list/">Dodaj/modyfikuj statystyki</a>' % obj.folder.id)
        show_firm_url.allow_tags = True

    add_files_folder.short_description = "Pliki statystyk"
    fields = ('name',)

    def has_add_permission(self, request):
        if Statistics.objects.all().count() == 0:
            return True

        return False

admin.site.register(FieldEvent, FieldEventAdmin)
admin.site.register(EventPlace, EventPlaceAdmin)
admin.site.register(Organizer, OrganizerAdmin)
admin.site.register(EventsGlobalSettings, EventsGlobalSettingsAdmin)
admin.site.register(Ranks, RanksAdmin)
admin.site.register(Records, RecordsAdmin)
admin.site.register(Statistics, StatisticsAdmin)
