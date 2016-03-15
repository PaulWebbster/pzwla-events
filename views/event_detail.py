# -*- coding: utf-8 -*-
from django.views.generic import DetailView
from ..models import FieldEvent


class EventDetailView(DetailView):
    model = FieldEvent
    context_object_name = 'field_event'

    def get_context_data(self, **kwargs):
        context = super(EventDetailView, self).get_context_data(**kwargs)

        field_event = FieldEvent.objects.get(slug=self.kwargs['slug'])
        datestr = field_event.date_time.strftime("%Y-%m-%dT%H:%M:%S")

        context['miliseconds'] = datestr

        return context
