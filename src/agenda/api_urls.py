from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from agenda import api_rest_views


router = DefaultRouter()
router.register(r'event', api_rest_views.EventViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
]