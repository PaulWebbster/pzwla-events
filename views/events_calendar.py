# -*- coding: utf-8 -*-
from django.views.generic import ListView
from ..models import FieldEvent
from ..models import EventsGlobalSettings


class EventCalendarView(ListView):
    context_object_name = 'competitions'
    template_name = 'pzwla_events/events_list.html'
    model = FieldEvent
    view_type = 'calendar'

    def get_queryset(self):
        default_year = EventsGlobalSettings.objects.all()[0].calendar_year

        return FieldEvent.objects.all().filter(date_time__year=default_year).order_by("date_time")

    def get_context_data(self, **kwargs):
        context = super(EventCalendarView, self).get_context_data(**kwargs)
        context['default_calendar_year'] = EventsGlobalSettings.objects.all()[0].calendar_year

        return context
