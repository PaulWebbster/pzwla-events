# -*- coding: utf-8 -*-
from django import template
from datetime import date
from urlparse import urlparse
from datetime import datetime
from django.contrib.sites.models import Site
from django.utils import timezone
from ..models import EventsGlobalSettings
from ..models import FieldEvent
from ..models import utc
from pzwla_events_plugin.models import ZawodyPlugin

register = template.Library()


@register.filter('is_future_year')
def is_future_year(value):
    return int(value) > date.today().year + 1


@register.filter
def future_date_invitation(value):
    calculated_diff = int(value)-date.today().year
    if calculated_diff == 1:
        return "Zapraszamy na tę stronę za rok"
    elif calculated_diff < 5:
        return "Zapraszamy na tę strona za %d lata" % calculated_diff
    else:
        return "Zapraszamy na tę stronę za %d lat" % calculated_diff


@register.filter
def is_calendar_view(value):
    return value == 'calendar'


@register.filter
def is_result_view(value):
    return value == 'result'


@register.inclusion_tag("pzwla_events/sub_menu/sub_menu_event.html")
def show_sub_menu(**kwargs):
    domain = Site.objects.get_current().domain
    context_dict = dict()

    event = kwargs['event']

    context_dict['event'] = event

    event_menu = [{'name': "Informacje",
                   'icon': "glyphicon-info-sign",
                   'href': "http://{domain}/zawody/{slug}".format(domain=domain, slug=event.slug)}]

    if timezone.now() <= event.date_time:
        if event.entries:
            event_menu.append({'name': "Zapisy",
                               'icon': "glyphicon-check",
                               'href': event.entries})

    if event.results_file:
        event_menu.append({'name': "Wyniki",
                           'icon': "glyphicon-list",
                           'href': event.results_file.url})
    elif event.results:
        event_menu.append({'name': "Wyniki",
                           'icon': "glyphicon-list",
                           'href': event.results})

    if event.timetable_file:
        event_menu.append({'name': 'Program',
                           'icon': 'glyphicon-time',
                           'href': event.timetable_file.url})
    elif event.timetable:
        event_menu.append({'name': 'Program',
                           'icon': 'glyphicon-time',
                           'href': event.timetable})

    if event.entry_booklet_file:
        event_menu.append({'name': 'Komunikat organizacyjny',
                           'icon': 'glyphicon-book',
                           'href': event.entry_booklet_file.url})
    elif event.entry_booklet:
        event_menu.append({'name': 'Komunikat organizacyjny',
                           'icon': 'glyphicon-book',
                           'href': event.entry_booklet})

    if event.team_file:
        event_menu.append({'name': 'Nasz kadra',
                           'icon': 'glyphicon-user',
                           'href': event.team_file.url})

    context_dict['event_menu'] = event_menu

    return context_dict


@register.inclusion_tag("pzwla_events/sub_menu/sub_menu_calendars.html")
def show_calendar_menu(**kwargs):
    context_dict = dict()

    context_dict['default_calendar_year'] = EventsGlobalSettings.objects.all()[0].calendar_year

    if kwargs['calendar']:
        context_dict['active_menu'] = True
    else:
        context_dict['active_menu'] = False

    return context_dict


@register.inclusion_tag("pzwla_events/sub_menu/sub_menu_results.html")
def show_results_menu(**kwargs):
    context_dict = dict()

    context_dict['default_result_year'] = EventsGlobalSettings.objects.all()[0].results_year

    if kwargs['results']:
        context_dict['active_menu'] = True
    else:
        context_dict['active_menu'] = False

    return context_dict


@register.inclusion_tag("pzwla_events/sub_menu/sub_menu_ranks.html")
def show_ranks_menu(**kwargs):
    context_dict = dict()

    context_dict['default_result_year'] = EventsGlobalSettings.objects.all()[0].results_year

    if kwargs['ranks']:
        context_dict['active_menu'] = True
    else:
        context_dict['active_menu'] = False

    return context_dict


@register.inclusion_tag("pzwla_events/sub_menu/sub_menu_info.html")
def show_info_menu(**kwargs):
    context_dict = dict()

    context_dict['default_result_year'] = EventsGlobalSettings.objects.all()[0].results_year

    if kwargs['info']:
        context_dict['active_menu'] = True
    else:
        context_dict['active_menu'] = False

    return context_dict


@register.inclusion_tag("pzwla_events/next_meeting.html", takes_context=True)
def show_next_meetings(context, **kwargs):
    settings = ZawodyPlugin.objects.all()[0]
    events = list()
    events_number = 0

    if settings.add_preferable:
        events_query = FieldEvent.objects.all().filter(preferable=True, date_time__gt=datetime.now(tz=utc))\
            .order_by('date_time')
        for event in events_query:
            events.append(event)
        events_number = len(events)

    for event in FieldEvent.objects.all().filter(date_time__gt=datetime.now(tz=utc)).order_by('date_time'):
        if event in events:
            continue
        if events_number > settings.events_number:
            break

        events.append(event)
        events_number += 1

    events.sort(key=lambda x: x.date_time)

    dates = list()

    for event in events:
        dates.append(event.date_time.strftime("%Y/%m/%d"))

    context['next_meetings'] = events
    context['next_meetings_dates'] = dates

    sezikai_ctx_var = getattr(settings, 'SEKIZAI_VARNAME', 'SEKIZAI_CONTENT_HOLDER')
    attrs = {
        'next_meetings': events,
        'next_meetings_dates': dates,
        sezikai_ctx_var: context[sezikai_ctx_var]
    }

    return attrs
