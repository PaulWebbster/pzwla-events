# -*- coding: utf-8 -*-
from django import template
from datetime import date
from urlparse import urlparse
from django.contrib.sites.models import Site

register = template.Library()


@register.filter
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


def lol():
    pass


@register.inclusion_tag("zawody/sub_menu/sub_menu_event.html")
def show_sub_menu(category, **kwargs):
    domain = Site.objects.get_current().domain
    context_dict = dict()

    if category == 'event_details':
        event = kwargs['event']

        context_dict['event'] = event

        event_menu = [{'name': "Informacje",
                       'icon': "glyphicon-info-sign",
                       'href': "http://{domain}/zawody/{acronym}".format(domain=domain, acronym=event.acronym)}]

        if event.entries is not None:
            event_menu.append({'name': "Zapisy",
                               'icon': "glyphicon-check",
                               'href': event.entries})

        if event.results is not None:
            event_menu.append({'name': "Wyniki",
                               'icon': "glyphicon-list",
                               'href': event.results})

        if event.timetable is not None:
            event_menu.append({'name': 'Program',
                               'icon': 'glyphicon-time',
                               'href': event.timetable})

        context_dict['event_menu'] = event_menu

        return context_dict

