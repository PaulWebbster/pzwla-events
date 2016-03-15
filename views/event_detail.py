# -*- coding: utf-8 -*-
from django.views.generic import DetailView
from ..models import FieldEvent


class EventDetailView(DetailView):
    model = FieldEvent
    context_object_name = 'field_event'
