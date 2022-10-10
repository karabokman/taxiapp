from django.urls import path
from .views import HomepageView, RoutemanagerView, RouteView,AllRoutesView,DeleteRouteView,AddTransactionView,AddRegisteredView,RemovePassengerView,MarkDoneView

urlpatterns = [
    path('',HomepageView.as_view(), name="homepage"),
    path('manage-route/?P<id>[0-9]+)\\Z',RoutemanagerView.as_view(), name="manage-route"),
    path('add-route-driver/',RouteView.as_view(), name="add-route-d"),
    path('all-routes/',AllRoutesView.as_view(), name="all-routes"),
    path('delete-route/?P<id>[0-9]+)\\Z',DeleteRouteView.as_view(), name="delete-route"),
    path('add-transaction-driver/?P<id>[0-9]+)\\Z',AddTransactionView.as_view(), name="add-transact"),
    path('add-registered-driver/?P<id>[0-9]+)\\Z',AddRegisteredView.as_view(), name="add-registered"),
    path('remove-passenger/?P<id>[0-9]+)\\Z',RemovePassengerView.as_view(), name="remove-passenger"),
    path('mark-route/?P<id>[0-9]+)\\Z',MarkDoneView.as_view(), name="mark-route"),

]
