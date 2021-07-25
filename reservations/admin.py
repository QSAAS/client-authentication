from django.contrib import admin
from reservations.models import QueueNode, Reservation

admin.site.register(QueueNode)
admin.site.register(Reservation)
