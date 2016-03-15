from django.views.generic.list import ListView
from ..models import FieldEvent


class ArchivalCalendarsView(ListView):
    context_object_name = 'archival_years'
    template_name = 'pzwla_events/archival_calendars.html'
    view_type = 'calendar'

    def get_queryset(self):
        events_years = []

        for event in FieldEvent.objects.all():
            if event.date_time.year not in events_years:
                events_years.append(event.date_time.year)

        return events_years

    def get_context_data(self, **kwargs):
        context = super(ArchivalCalendarsView, self).get_context_data(**kwargs)
        context['calendar_object'] = True

        return context
