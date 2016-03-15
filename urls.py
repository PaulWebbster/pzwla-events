from django.conf.urls import url

from views import ArchivalResultsView
from views import EventCalendarView
from views import EventsResultsView
from views import ArchivalCalendarsView
from views import EventDetailView
from views import EventInfoView

urlpatterns = [
    #url(r'^(?P<acronym>[A-Z]{4,11}\d{4}[A-Z]{2,3})/', FieldEventDetailsView.as_view()),
    url(r'^kalendarz/(?P<year>\w+)?$', EventCalendarView.as_view()),
    url(r'^kalendarz/archiwum/?$', ArchivalCalendarsView.as_view()),
    url(r'^wyniki/archiwum/?$', ArchivalResultsView.as_view()),
    url(r'^wyniki/(?P<year>\w+)?/?$', EventsResultsView.as_view()),
    url(r'^informacje-o-zawodach/(?P<year>\w+)?$', EventInfoView.as_view()),
    url(r'^(?P<slug>[-\w]+)/$', EventDetailView.as_view(), name='event-detail'),
]
