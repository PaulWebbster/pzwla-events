# -*- coding: utf-8 -*-
from django import template
from datetime import date
from urlparse import urlparse
from datetime import datetime
from django.contrib.sites.models import Site
from django.utils import timezone
from ..models import EventsGlobalSettings

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
