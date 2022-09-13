import json
from lib2to3.pgen2 import driver
from urllib import request
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework_simplejwt.views import TokenObtainPairView
from itertools import groupby


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





    def get_queryset(self):
        user = self.request.user
        if user.group == 'driver':
            trip = Trip.objects.filter(Q(status='REQUESTED'))
            
            return trip
                          
        if user.group == 'passenger':
            trip = Trip.objects.filter(Q(status='ACCEPTED'))
            return trip
            
        
        return Trip.objects.none()

    # list 'id', 'created', 'updated', 'pick_up_address', 'drop_off_address', 'price'
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = NestedTripSerializer(queryset, many=True, context={'request': request})
        
        data = {
            'id': serializer.data[0]['id'],
            'created': serializer.data[0]['created'],
            'updated': serializer.data[0]['updated'],
            'pick_up_address': serializer.data[0]['pick_up_address'],
            'drop_off_address': serializer.data[0]['drop_off_address'],
            'price': serializer.data[0]['price'],
            'passsenger__name': serializer.data[0]['passenger']['first_name'],
            'passenger__email': serializer.data[0]['passenger']['email'],
            'driver__name': serializer.data[0]['driver']['first_name'],
            'driver__email': serializer.data[0]['driver']['email'],
            

        }
        return Response(data)



        
 
    
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

#convert trip_id



    
    




