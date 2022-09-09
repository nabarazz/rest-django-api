from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Trip
from .serializers import LogInSerializer, UserSerializer, NestedTripSerializer, TripSerializer


class SignUpView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class LogInView(TokenObtainPairView):

    queryset = get_user_model().objects.all()
    serializer_class = LogInSerializer


class TripView(generics.ListCreateAPIView):
    lookup_field = 'id'
    lookup_url_kwarg = 'trip_id'
    serializer_class = NestedTripSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if user.group == 'driver':
            return Trip.objects.filter(
                Q(status=Trip.REQUESTED) | Q(driver=user)
            )
        if user.group == 'rider':
            return Trip.objects.filter(rider=user)
        return Trip.objects.none()
