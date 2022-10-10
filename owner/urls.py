from django.urls import path
from .views import DashBoardView,AddRouteView, AddDestination, PassengersView,DriversView,TaxisView,HireRequestView, RequestVieW, AddDriverView, RouteView,DestView,PassProfileView,EditTaxiView,EditDriverView,TodolistView,DeleteTaskView,MarkTaskView,DeleteDriverView,DeleteTaxiView, TransactionView,DeleteRequestView

urlpatterns = [
    path('',DashBoardView.as_view(), name="dashboard"),
    path('add-route/',AddRouteView.as_view(), name="add-route"),
    path('add-driver/',AddDriverView.as_view(), name="add-driver"),
    path('add-destination/',AddDestination.as_view(), name="add-destination"),
    path('view-passengers/',PassengersView.as_view(), name="view-passengers"),
    path('view-drivers/',DriversView.as_view(), name="view-drivers"),
    path('view-taxis/',TaxisView.as_view(), name="view-taxis"),
    path('view-hire-requests/', HireRequestView.as_view(), name="hire-requests"),
    path('request-edit/?P<id>[0-9]+)\\Z', RequestVieW.as_view(), name="request-edit"),
    path('view-route/?P<id>[0-9]+)\\Z', RouteView.as_view(), name="view-route"),
    path('all-destination/', DestView.as_view(), name="all-dest"),
    path('view-profile/?P<id>[0-9]+)\\Z', PassProfileView.as_view(), name="view-profile"),
    path('edit-taxi/?P<id>[0-9]+)\\Z', EditTaxiView.as_view(), name="edit-taxi"),
    path('edit-driver/?P<id>[0-9]+)\\Z', EditDriverView.as_view(), name="edit-driver"),
    path('to-do-list/', TodolistView.as_view(), name="todolist"),
    path('delete-task/?P<id>[0-9]+)\\Z', DeleteTaskView.as_view(), name="delete-task"),
    path('mark-task/?P<id>[0-9]+)\\Z', MarkTaskView.as_view(), name="mark-task"),
    path('delete-driver/?P<id>[0-9]+)\\Z', DeleteDriverView.as_view(), name="delete-driver"),
    path('delete-taxi/?P<id>[0-9]+)\\Z', DeleteTaxiView.as_view(), name="delete-taxi"),
    path('delete-request/?P<id>[0-9]+)\\Z', DeleteRequestView.as_view(), name="delete-request"),
    path('transactions/', TransactionView.as_view(), name="transactions"),

]
