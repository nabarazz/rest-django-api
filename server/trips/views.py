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

    # desplay only nestedtripserializer id only on response
    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data['id'])

    def get_queryset(self):
        user = self.request.user
        if user.group == 'passenger':
            #request to all drivers
            return Trip.objects.filter(Q(passenger=user) | Q(status='ACCEPTED')
            print('passenger')

        if user.group == 'driver':
            #request to all passengers
            return Trip.objects.filter(Q(driver=user) | Q(status=Trip.REQUESTED))
            print('driver')

            
        return Trip.objects.none()
 
    
class CreateTripView(generics.CreateAPIView):
    serializer_class = NestedTripSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(passenger=self.request.user)
        print('create')

    




