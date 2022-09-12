from django.urls import path


from .views import TripView, CreateTripView


app_name = 'taxi'

urlpatterns = [
    path('', TripView.as_view({'get': 'list'}), name='trip'),
    path('<uuid:trip_id>/', TripView.as_view({'get': 'retrieve'}), name='trip'),
    path('create/', CreateTripView.as_view(), name='create_trip'),

]

# urlpatterns = [
#     path('', TripView.as_view(), name='trip'),
#     path('<uuid:trip_id>/', TripView.as_view(), name='trip'),
    

# ]


    # path('', TripView.as_view({'get': 'list'}), name='trip_list'),
    # path('<uuid:trip_id>/', TripView.as_view({'get': 'retrieve'}), name='trip_detail'),
