from django.conf.urls import url
from views import FieldEventDetailsView, EventCalendarView, EventsResultsView, ArchivalCalendarsView
from views import ArchivalResultsView

urlpatterns = [
    url(r'^(?P<acronym>[A-Z]{4,11}\d{4}[A-Z]{2,3})/', FieldEventDetailsView.as_view()),
    url(r'^kalendarz/archiwum/?$', ArchivalCalendarsView.as_view()),
    url(r'^kalendarz/(?P<year>\w+)?/?(?P<type>\w+)?/?$', EventCalendarView.as_view()),
    url(r'^wyniki/archiwum/?$', ArchivalResultsView.as_view()),
    url(r'^wyniki/(?P<year>\w+)?/?(?P<type>\w+)?/?$', EventsResultsView.as_view()),
]
