# -*- coding: utf-8 -*-
from django.views.generic.list import ListView
from ..models import EventsGlobalSettings
from ..models import Records


class StatisticsView(ListView):
    template_name = 'pzwla_events/stats.html'
    view_type = 'stats'
    model = Records
    context_object_name = 'stats'

    def get_context_data(self, **kwargs):
        context = super(StatisticsView, self).get_context_data(**kwargs)

        context['stats_files'] = context['stats'][0].get_records_files

        return context
