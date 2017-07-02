import datetime
import time

from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from django.db.models import Q

from agenda import models
from agenda import serializers


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Event.objects.all()
    model = models.Event
    # parser_classes = (JSONParser,)
    serializer_class = serializers.EventSerializer

    def get_queryset(self):
        # import ipdb; ipdb.set_trace()
        queryset = models.Event.objects.all()
        event_date = self.request.GET.get('date', None)
        if event_date:
            try:
                # 21-06-2017
                event_date = datetime.datetime.strptime(event_date, '%d-%m-%Y')
            except ValueError:
                event_date = None
            if event_date:
                queryset = queryset.filter(start__contains=event_date.date())

        location = self.request.GET.get('location', None)
        if location:
            queryset = queryset.filter(location__contains=location)

        text = self.request.GET.get('text', None)
        if text:
            queryset = queryset.filter(Q(summary__contains=text) | Q(description__contains=text))

        next = self.request.GET.get('next', None)
        if next:
            now = datetime.datetime.now()
            now = datetime.datetime(2016, 10, 8, 15, 0, 0)
            queryset = queryset.filter(start__gte=now)
            return queryset.order_by('start')[:3]
        else:
            return queryset.order_by('start')