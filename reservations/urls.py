from django.urls import path
from reservations.views import ReservationCreateView

urlpatterns = [
    path("", ReservationCreateView.as_view())
]
