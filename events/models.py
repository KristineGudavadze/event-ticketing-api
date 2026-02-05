from django.db import models
from django.conf import settings
import uuid

class Event(models.Model):

    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="organized_events"
    )

    title = models.CharField(max_length=255)
    description = models.TextField()

    date = models.DateTimeField()

    capacity = models.PositiveIntegerField()
    ticket_sold = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Ticket(models.Model):

    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("USED", "Used"),
        ("CANCELLED", "Cancelled"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tickets"
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="tickets"
    )

    qt_token = models.UUIDField(
        default=uuid.uuid4,
        unique=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ACTIVE"
    )

    purchased_at = models.DateTimeField(auto_now_add=True)

class Meta:
    unique_together = ["user", "event"]