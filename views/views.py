# -*- coding: utf-8 -*-
from datetime import tzinfo, timedelta, datetime
from django.views.generic.list import ListView
from ..models import FieldEvent
from ..models import EventsGlobalSettings

ZERO = timedelta(0)


class UTC(tzinfo):
    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO


utc = UTC()


class CompetitionViewBase(ListView):
    # region Fields
    """
    View type field describes what kind of view is. Based on the type of
    view the url parsing as well side bar context is properly generated.
    """
    view_type = None

    # endregion Fields

    def get_context_data(self, **kwargs):
        context = super(CompetitionViewBase, self).get_context_data(**kwargs)
        context['default_calendar_year'] = self.get_year_from_url()
        context['default_result_year'] = self.get_year_from_url(type_setting="result")
        self.get_sidebar_context(context)
        self.get_menu_special_events(context)
        self.get_next_meetings(context)
        self.get_last_meetings(context)

        return context

    def get_sidebar_context(self, context):
        # calendar_categories = EventCategory.objects.all()
        calendar_categories_dict = dict()
        results_categories_dict = dict()

        default_year_calendar = self.get_year_from_url()
        default_year_results = self.get_year_from_url(type_setting='result')
        '''
        for category in calendar_categories:
            counts = FieldEvent.objects.all().filter(event_category=category,
                                                     date_time__year=default_year_calendar).count()
            calendar_categories_dict[category] = counts

            counts = FieldEvent.objects.all().filter(event_category=category,
                                                     date_time__year=default_year_results).count()
            results_categories_dict[category] = counts
            '''

        context['menu_calendar'] = calendar_categories_dict
        context['menu_results'] = results_categories_dict

        context['all_calendar_events_count'] = FieldEvent.objects.all() \
            .filter(date_time__year=default_year_calendar).count()

        context['all_results_events_count'] = FieldEvent.objects.all() \
            .filter(date_time__year=default_year_results).count()

        context['active_menu'] = self.view_type

        return context

    @staticmethod
    def get_next_meetings(context, number=4):
        events = FieldEvent.objects.all().filter(date_time__gt=datetime.now(tz=utc)).order_by("date_time")[:4]

        context['next_meetings'] = events

        dates = list()
        for event in events:
            dates.append(event.date_time.strftime("%Y/%m/%d"))

        context['next_meetings_dates'] = dates

    @staticmethod
    def get_last_meetings(context, number=4):
        events = FieldEvent.objects.all().filter(date_time__lt=datetime.now(tz=utc)).order_by("date_time")

        context['last_meetings'] = events

    @staticmethod
    def get_menu_special_events(context):
        context['special_events'] = FieldEvent.objects.all().filter(preferable=True)

    '''
    def get_desired_category(self):
        for category in EventCategory.objects.all():
            if category.acronym == self.kwargs['type']:
                return category
    '''

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


class FieldEventDetailsView(CompetitionViewBase):
    context_object_name = 'event_detail'
    template_name = 'zawody/event_details.html'
    model = FieldEvent
    view_type = 'event_details'

    def get_context_data(self, **kwargs):
        context = super(FieldEventDetailsView, self).get_context_data(**kwargs)

        field_event = FieldEvent.objects.get(acronym=self.kwargs['acronym'])
        organizer = field_event.organizer
        event_place = field_event.place
        datestr = field_event.date_time.strftime("%Y-%m-%dT%H:%M:%S")
        lattitude = "%0.4f" % field_event.position.latitude
        longitude = "%0.4f" % field_event.position.longitude

        context['field_event'] = field_event
        context['organizer'] = organizer
        context['event_place'] = event_place
        context['miliseconds'] = datestr
        context['lattitude'] = lattitude
        context['longitude'] = longitude

        return context


class EventsResultsView(CompetitionViewBase):
    context_object_name = 'events_results'
    template_name = 'zawody/events_results.html'
    model = FieldEvent
    view_type = 'result'

    months = ["styczeń", "luty", "marzec", "kwiecień", "maj", "czerwiec", "lipiec", "sierpień", "wrzesień",
              "październik", "listopad", "grudzień"]

    def get_queryset(self):

        desired_category = self.get_desired_category()
        result_year = self.get_year_from_url(type_setting=self.view_type)

        months_events = dict()

        if self.kwargs['type'] is not None:
            for i, month in enumerate(self.months, start=1):
                events = FieldEvent.objects.all().filter(event_category=desired_category,
                                                         date_time__year=result_year,
                                                         date_time__lte=datetime.today(),
                                                         date_time__month=i).order_by("date_time")
                if len(events) != 0:
                    months_events[month] = events
        else:
            for i, month in enumerate(self.months, start=1):
                events = FieldEvent.objects.all().filter(date_time__year=result_year,
                                                         date_time__lte=datetime.today(),
                                                         date_time__month=i).order_by("date_time")
                if len(events) != 0:
                    months_events[month] = events

        result_dict = dict()

        result_dict['months_order'] = self.months
        result_dict['months_events'] = months_events

        return result_dict

    def get_context_data(self, **kwargs):
        context = super(EventsResultsView, self).get_context_data(**kwargs)

        # Pobranie kategorii przeglądanych wyników zawodów
        if self.get_desired_category() is not None:
            context['event_category'] = self.get_desired_category()
        else:
            context['event_category'] = "Wszystkie zawody"

        # Pobranie roku przeglądanych wyników zawodów
        context['events_year'] = self.get_year_from_url(type_setting=self.view_type)

        return context


class ArchivalCalendarsView(CompetitionViewBase):
    context_object_name = 'archival_years'
    template_name = 'zawody/archival_calendars.html'
    view_type = 'calendar'

    def get_queryset(self):
        events_years = []

        for event in FieldEvent.objects.all():
            if event.date_time.year not in events_years:
                events_years.append(event.date_time.year)

        return events_years


class ArchivalResultsView(CompetitionViewBase):
    context_object_name = 'archival_years'
    template_name = 'zawody/archival_results.html'
    view_type = 'result'

    def get_queryset(self):
        events_years = []

        for event in FieldEvent.objects.all():
            if event.date_time.year not in events_years:
                events_years.append(event.date_time.year)

        return events_years
