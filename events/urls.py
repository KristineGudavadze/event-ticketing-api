from rest_framework import routers
from .views import EvenViewSet, TicketViewSet
from django.urls import path, include


router = routers.DefaultRouter()
router.register(r'events', EvenViewSet)
router.register(r'tickets', TicketViewSet)

urlpatterns = [
    path('', include(router.urls)),
]