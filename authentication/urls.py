from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from authentication.views import RegisterView, DummyView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', RegisterView.as_view()),
    path('dummy/', DummyView.as_view())
]
