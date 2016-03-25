# -*- coding: utf-8 -*-
from django.views.generic.list import ListView
from ..models import EventsGlobalSettings
from ..models import Ranks


class RanksView(ListView):
    template_name = 'pzwla_events/ranks.html'
    view_type = 'records'
    model = Ranks
    context_object_name = 'records'

    def get_context_data(self, **kwargs):
        context = super(RanksView, self).get_context_data(**kwargs)
        # Pobranie roku przeglądanych wyników zawodów
        context['ranks_year'] = self.get_year_from_url(type_setting='result')

        # Pobranie rankingow
        context['ranks'] = Ranks.objects.get(ranks_year=context['ranks_year']).get_rank_files

        context['ranks_object'] = True

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
