from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from reservations.serializers import ReservationCreationSerializer
from rest_framework.response import Response
from django.core import serializers as core_serializer
from reservations.services import publish_event
from rest_framework import status


class ReservationCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = ReservationCreationSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        reservation = serializer.save()

        print(reservation)
        # serializing reservation (model instance => python dictionary)
        reservation_data = core_serializer.serialize('python', [reservation, ])[0]
        reservation_id = reservation_data["pk"]
        number_in_queue = reservation.queue_node.last_number_in_queue
        reservation_data["number_in_queue"] = number_in_queue

        # reformat dictionary
        reservation_data = reservation_data["fields"]
        reservation_data["reservation_id"] = reservation_id

        # raise event
        publish_event(reservation_data)

        headers = self.get_success_headers(serializer.data)
        return Response(reservation_data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)


