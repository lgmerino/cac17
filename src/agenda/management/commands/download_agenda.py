import time
import datetime
import requests
from lxml import etree

from django.core.management.base import BaseCommand

from agenda.models import Event


class Command(BaseCommand):
    args = ''
    help = ''
    URL_XCAL = 'http://2016.es.pycon.org/schedule/xcal.xml'
    SUMMARY = 'summary'
    DESCRIPTION = 'description'
    LOCATION = 'location'
    START = 'dtstart'
    END = 'dtend'

    def get_text(self, node):
        return node[0].text or 'N/A'

    def get_datetime(self, node):
        try:
            value = datetime.datetime.strptime(node[0].text, '%Y-%m-%dT%H:%M:%S')
        except:
            value = None
        return value

    def handle(self, *args, **options):
        t1 = time.time()
        print("\nSTARTING download_agenda")

        data = []
        tags = {self.SUMMARY: self.get_text,
                self.DESCRIPTION: self.get_text,
                self.LOCATION: lambda x: x.text or 'N/A',
                self.START: self.get_datetime,
                self.END: self.get_datetime}

        request = requests.get(self.URL_XCAL)
        root = etree.fromstring(request.text.replace(' xmlns="urn:ietf:params:xml:ns:icalendar-2.0"', ''))
        vcalendar = root[0]

        for vevent in vcalendar:
            event = Event()
            properties = vevent[0]
            for child in properties:
                if child.tag == self.START:
                    field_name = 'start'
                elif child.tag == self.END:
                    field_name = 'end'
                else:
                    field_name = child.tag
                setattr(event, field_name, tags[child.tag](child))
            # buscamos evento por titulo antes de salvar
            try:
                existing_event = Event.objects.get(summary=getattr(event, self.SUMMARY))
                existing_event.start = event.start
                existing_event.end = event.end
                existing_event.description = event.description
                existing_event.location = event.location
                existing_event.save()
            except Event.DoesNotExist:
                event.save()
            except Event.MultipleObjectsReturned:
                # es el cafe, pasamos
                pass

        t2 = time.time()
        # RESULTADO
        result = "Executed index_database.py in %0.3f ms\n" % ((t2 - t1) * 1000.0)
        print(result)
        return result