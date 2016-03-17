# -*- coding: utf-8 -*-
from django.views.generic.list import ListView
from ..models import EventsGlobalSettings
from ..models import Records


class RecordsView(ListView):
    template_name = 'pzwla_events/records.html'
    view_type = 'records'
    model = Records
    context_object_name = 'records'

    def get_context_data(self, **kwargs):
        context = super(RecordsView, self).get_context_data(**kwargs)

        context['records_files'] = context['records'][0].get_records_files

        return context
