from django.conf.urls import url

from views import ArchivalResultsView
from views import EventCalendarView
from views import EventsResultsView
from views import ArchivalCalendarsView
from views import EventDetailView

urlpatterns = [
    #url(r'^(?P<acronym>[A-Z]{4,11}\d{4}[A-Z]{2,3})/', FieldEventDetailsView.as_view()),
    url(r'^kalendarz/$', EventCalendarView.as_view()),
    url(r'^(?P<slug>[-\w]+)/$', EventDetailView.as_view(), name='event-detail'),
    url(r'^kalendarz/archiwum/?$', ArchivalCalendarsView.as_view()),
    url(r'^wyniki/archiwum/?$', ArchivalResultsView.as_view()),
    url(r'^wyniki/(?P<year>\w+)?/?(?P<type>\w+)?/?$', EventsResultsView.as_view()),
]
