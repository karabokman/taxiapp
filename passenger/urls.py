from django.urls import path
from .views import IndexView, ProfileView, DestinationView, RideHistoryView,BookingView,HireTaxiView

urlpatterns = [
    path('',IndexView.as_view(), name="passenger"),
    path('profile/',ProfileView.as_view(), name="profile"),
    path('destinations/',DestinationView.as_view(), name="destinations"),
    path('history/',RideHistoryView.as_view(), name="history"),
    path('view-destination/?P<id>[0-9]+)\\Z',BookingView.as_view(), name="booking"),
    path('hire-taxi/',HireTaxiView.as_view(), name="hire-taxi"),

]
