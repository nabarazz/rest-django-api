from lib2to3.pgen2 import driver
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import generics, permissions, viewsets
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



    

class TripView(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'id'
    lookup_url_kwarg = 'trip_id'
    
    serializer_class = NestedTripSerializer
    permission_classes = (permissions.IsAuthenticated,)

    # call only id and status field of trip model
    
        


    def get_queryset(self):
        user = self.request.user

        if user.group == 'passenger':
            #request to all drivers
            passenger_trip = Trip.objects.filter(Q(passenger=user))
            #pop driver and passenger field and add passenger.email and passenger.username

            passenger_trip = passenger_trip.values('id', 'status', 'pick_up_address', 'drop_off_address', 'created', 'updated', 'passenger__email', 'passenger__username')
            #add passenger email
            
            
            

            # retrieve passenger id and status
            return passenger_trip
            
            

        if user.group == 'driver':
            #request to all passengers
            driver_trip = Trip.objects.filter(Q(driver=user) & Q(status=Trip.REQUESTED))

            #pop driver and passenger field 
            driver_trip = driver_trip.values('id', 'status', 'pick_up_address', 'drop_off_address', 'created', 'updated')
            #add user.email on driver_trip 
            
            return driver_trip
            print('driver')

            
        return Trip.objects.none()
 
    
class CreateTripView(generics.CreateAPIView):
    serializer_class = NestedTripSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(passenger=self.request.user)
        print('create')

    




