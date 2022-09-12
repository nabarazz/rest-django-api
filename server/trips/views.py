from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView


from taxi.middleware import get_user


from .models import Trip
from .serializers import LogInSerializer, UserSerializer, TripDriverSerializer, TripPassengerSerializer


class SignUpView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class LogInView(TokenObtainPairView):

    queryset = get_user_model().objects.all()
    serializer_class = LogInSerializer



class DriverTripView(generics.ListCreateAPIView):
    lookup_field = 'id'
    lookup_url_kwarg = 'trip_id'
    serializer_class = TripDriverSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        # serializer.save(passenger=self.request.user)
        serializer.save(driver=self.request.user)
        print(serializer.data)

        
    def get_queryset(self):
        user = self.request.user
        if user.group == 'driver':
            return Trip.objects.filter(
                Q(status=Trip.REQUESTED) | Q(driver=user)
            )
        # if user.group == 'passenger':
        #     return Trip.objects.filter(passenger=user)
        return Trip.objects.none()

class PassengerTripView(generics.ListCreateAPIView):
    lookup_field = 'id'
    lookup_url_kwarg = 'trip_id'
    serializer_class = TripPassengerSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(passenger=self.request.user)
        print(serializer.data)

    def get_queryset(self):
        user = self.request.user
        if user.group == 'passenger':
            return Trip.objects.filter(passenger=user)
        return Trip.objects.none()

    




