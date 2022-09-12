from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView


from taxi.middleware import get_user


from .models import Trip
from .serializers import LogInSerializer, UserSerializer, NestedTripSerializer


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
        if user.group == 'passenger':
            #request to all drivers
            return Trip.objects.filter(passenger=user)

        if user.group == 'driver':
            #request to all passengers
            return Trip.objects.filter(Q(driver=user) | Q(status=Trip.REQUESTED))

            # return Trip.objects.filter(passenger=user)
        return Trip.objects.none()
 
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if serializer.data['status'] == 'ACCEPTED':
            Trip.objects.filter(~Q(id=instance.id)).filter(
                driver=instance.driver
            ).update(status=Trip.CANCELED)
        return Response(serializer.data)

    




