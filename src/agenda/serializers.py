from rest_framework import serializers

from agenda import models


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = ('id',
                  'summary',
                  'location',
                  'description',
                  'start',
                  'end',)
