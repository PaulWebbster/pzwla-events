from django.conf.urls import url
from django.views.generic import TemplateView

from views import ArchivalResultsView
from views import EventCalendarView
from views import EventsResultsView
from views import ArchivalCalendarsView
from views import ArchivalInfoView
from views import EventDetailView
from views import EventInfoView
from views import RecordsView
from views import StatisticsView
from views import RanksView

urlpatterns = [
    #url(r'^(?P<acronym>[A-Z]{4,11}\d{4}[A-Z]{2,3})/', FieldEventDetailsView.as_view()),
    url(r'^kalendarz/$', EventCalendarView.as_view()),
    url(r'^kalendarz/archiwum/?$', ArchivalCalendarsView.as_view()),
    url(r'^kalendarz/(?P<year>\w+)/$', EventCalendarView.as_view()),
    url(r'^wyniki/archiwum/?$', ArchivalResultsView.as_view()),
    url(r'^wyniki/$', EventsResultsView.as_view()),
    url(r'^wyniki/(?P<year>\w+)/$', EventsResultsView.as_view()),
    url(r'^rankingi/$', RanksView.as_view()),
    url(r'^rankingi/(?P<year>\w+)/$', RanksView.as_view()),
    url(r'^informacje-o-zawodach/$', EventInfoView.as_view()),
    url(r'^informacje-o-zawodach/archiwum/$', ArchivalInfoView.as_view()),
    url(r'^informacje-o-zawodach/(?P<year>\w+)/$', EventInfoView.as_view()),
    url(r'^rekordy/?$', RecordsView.as_view()),
    url(r'^statystyki/?$', StatisticsView.as_view()),
    url(r'^non-stadia/?$', TemplateView.as_view(template_name='pzwla_events/non-stadia.html')),
    url(r'^chod-sportowy/?$', TemplateView.as_view(template_name='pzwla_events/chod-sportowy.html')),
    url(r'^kalkulator-wynikow/?$', TemplateView.as_view(template_name='pzwla_events/kalkulator.html')),
    url(r'^(?P<slug>[-\w]+)/$', EventDetailView.as_view(), name='event-detail'),
]
