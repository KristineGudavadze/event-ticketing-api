from rest_framework import viewsets
from .models import Event, Ticket
from .serializers import EventSerializer, TicketSerializer
from rest_framework.permissions import IsAdminUser


class EvenViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAdminUser]