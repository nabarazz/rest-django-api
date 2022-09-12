from django.urls import path


from .views import DriverTripView, PassengerTripView


app_name = 'taxi'

urlpatterns = [
    path('driver/', DriverTripView.as_view(), name='driver'),
    path('driver/<uuid:trip_id>/', DriverTripView.as_view(), name='driver'),
    path('passenger/', PassengerTripView.as_view(), name='passenger'),
    path('passenger/<uuid:trip_id>/', PassengerTripView.as_view(), name='passenger'),
]

# urlpatterns = [
#     path('', TripView.as_view(), name='trip'),
#     path('<uuid:trip_id>/', TripView.as_view(), name='trip'),
    

# ]


    # path('', TripView.as_view({'get': 'list'}), name='trip_list'),
    # path('<uuid:trip_id>/', TripView.as_view({'get': 'retrieve'}), name='trip_detail'),
