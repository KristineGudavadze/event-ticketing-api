import uuid

from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Event, Ticket
from .serializers import EventSerializer, TicketSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('-id')
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def purchase(self, request, pk=None):
        event = self.get_object()

        if Ticket.objects.filter(event=event, user=request.user).exists():
            return Response(
                {"error": "You have already purchased a ticket for this event."},
                status=status.HTTP_400_BAD_REQUEST
            )

        ticket = Ticket.objects.create(
            event=event,
            user=request.user,
            qr_token=str(uuid.uuid4())
        )

        serializer = TicketSerializer(ticket)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all().order_by('-id')
    serializer_class = TicketSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['post'])
    def validate(self, request):
        qr_token = request.data.get("qr_token")

        if not qr_token:
            return Response(
                {"detail': 'qr token is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            ticket = Ticket.objects.get(qr_token=qr_token)
        except Ticket.DoesNotExist:
            return Response(
                {"detail": "Invalid ticket"},
                status=status.HTTP_404_NOT_FOUND
            )

        if ticket.status == "USED":
            return Response(
                {"detail": "ticket already used"},
                status=status.HTTP_400_BAD_REQUEST
            )

        ticket.status = "USED"
        ticket.save(update_fields=["status"])

        return Response(
            {"detail': 'Ticket validated successfully"},
            status=status.HTTP_200_OK
        )
