from django.db.models import F
from django.db import transaction
from rest_framework import serializers
from reservations.models import Reservation, QueueNode


class ReservationCreationSerializer(serializers.Serializer):
    queue_node_id = serializers.UUIDField()

    def create(self, validated_data):
        node_id = validated_data["id"]
        request = self.context["request"]

        # atomic operation, if any function fails, all changes are rolled back
        with transaction.atomic():
            queue_node, _ = QueueNode.objects.get_or_create(id=node_id)
            queue_node.last_number_in_queue = F("last_number_in_queue") + 1
            queue_node.save(update_fields=["last_number_in_queue"])

            return Reservation.objects.create(
                client=request.user,
                queue_node=queue_node,
            )
