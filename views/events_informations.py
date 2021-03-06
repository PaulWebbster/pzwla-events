# -*- coding: utf-8 -*-
from django.views.generic import ListView
from ..models import FieldEvent
from ..models import EventsGlobalSettings


class EventInfoView(ListView):
    context_object_name = 'competitions'
    template_name = 'pzwla_events/info.html'
    model = FieldEvent
    view_type = 'calendar'

    def get_queryset(self):
        default_year = self.get_year_from_url()

        return FieldEvent.objects.all().filter(date_time__year=default_year).order_by("date_time")

    def get_context_data(self, **kwargs):
        context = super(EventInfoView, self).get_context_data(**kwargs)
        context['default_calendar_year'] = self.get_year_from_url()
        context['info_object'] = True

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
