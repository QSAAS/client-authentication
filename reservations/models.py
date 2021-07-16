import uuid

from django.db import models
from django.contrib.auth import get_user_model


class QueueNode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    last_number_in_queue = models.SmallIntegerField(default=0)


class Reservation(models.Model):
    reservation_id = models.AutoField(primary_key=True)
    client = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="reservations",
    )
    queue_node = models.ForeignKey(
        QueueNode,
        on_delete=models.CASCADE,
        related_name="reservations",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    verification_number = models.UUIDField(default=uuid.uuid4)
