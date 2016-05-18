# -*- coding: utf-8 -*-
from django.views.generic.list import ListView
from ..models import FieldEvent
from ..models import EventsGlobalSettings
from ..models import Ranks
from datetime import datetime
from django.db.models import Q


class EventsResultsView(ListView):
    context_object_name = 'events_results'
    template_name = 'pzwla_events/events_results.html'
    model = FieldEvent
    view_type = 'result'

    months = ["styczeń", "luty", "marzec", "kwiecień", "maj", "czerwiec", "lipiec", "sierpień", "wrzesień",
              "październik", "listopad", "grudzień"]

    def get_queryset(self):
        result_year = self.get_year_from_url(type_setting=self.view_type)

        months_events = dict()

        for i, month in enumerate(self.months, start=1):
            events = FieldEvent.objects.all().filter(date_time__year=result_year, date_time__lte=datetime.today(),
                                                     date_time__month=i, )\
                                             .exclude(Q(entry_booklet='') & Q(entry_booklet_file=''))\
                                             .order_by("date_time")
            if len(events) != 0:
                months_events[month] = events

        result_dict = dict()

        result_dict['months_order'] = self.months
        result_dict['months_events'] = months_events

        return result_dict

    def get_context_data(self, **kwargs):
        context = super(EventsResultsView, self).get_context_data(**kwargs)

        # Pobranie kategorii przeglądanych wyników zawodów
        context['event_category'] = "Wszystkie zawody"

        # Pobranie roku przeglądanych wyników zawodów
        context['events_year'] = self.get_year_from_url(type_setting=self.view_type)

        # Pobranie rankingow
        context['ranks'] = Ranks.objects.get(ranks_year=context['events_year']).get_rank_files

        context['results_object'] = True

        return context

    def get_year_from_url(self, type_setting="calendar"):
        """
        Returns the year for which, depending on url and global setting should
        be the date displayed.

        :param type_setting: One of setting 'calendar' or 'result'
        :return: String with year in fromat YYYY
        """
        if 'year' in self.kwargs:
            if self.kwargs['year'] is not None:
                return int(self.kwargs['year'])

        if type_setting == "calendar":
            return self.get_global_settings()['calendar_year']
        elif type_setting == "result":
            return self.get_global_settings()['results_year']

    @staticmethod
    def get_global_settings():
        global_settings = dict()
        global_settings['calendar_year'] = EventsGlobalSettings.objects.values("calendar_year")[0]['calendar_year']
        global_settings['results_year'] = EventsGlobalSettings.objects.values("results_year")[0]['results_year']

        return global_settings
