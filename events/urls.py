from rest_framework import routers
from .views import EventViewSet, TicketViewSet
from django.urls import path, include


router = routers.DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'tickets', TicketViewSet)

urlpatterns = [
    path('', include(router.urls)),
]