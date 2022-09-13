from lib2to3.pgen2 import driver
from urllib import request
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

    #filiter serializer_class field
    
    
        


    def get_queryset(self):
        user = self.request.user
        if user.group == 'driver':
            trip = Trip.objects.filter(Q(status='REQUESTED'))          #only return status='REQUESTED' data
            return trip.values('id', 'status', 'created', 'updated', 'price', 'pick_up_address', 'drop_off_address')
            
        if user.group == 'passenger':
            return Trip.objects.filter(Q(status='ACCEPTED')).values('id', 'status', 'created', 'updated', 'price', 'pick_up_address', 'drop_off_address')
        
        return Trip.objects.none()
 
    
class CreateTripView(generics.CreateAPIView):
    serializer_class = NestedTripSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(passenger=self.request.user)
        print('create')

    def get_queryset(self):
        user = self.request.user
        
            
        if user.group == 'passenger':
            return Trip.objects.filter(user.group == 'passenger')
        
        return Trip.objects.none()

    




