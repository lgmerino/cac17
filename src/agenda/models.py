from django.db import models
from django.utils.translation import ugettext_lazy as _


class Event(models.Model):
    summary = models.CharField(max_length=250, blank=True)
    description = models.TextField()
    location = models.CharField(max_length=100)
    start = models.DateTimeField()
    end = models.DateTimeField()

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        ordering = ['start']

    def __unicode__(self):
        return u"%s (%s)" %\
            (self.summary if self.summary else _("[No summary]"),
             self.location if self.location else _("[No location]"))

    def __str__(self):
        return u"%s (%s)" %\
            (self.summary if self.summary else _("[No summary]"),
             self.location if self.location else _("[No location]"))
