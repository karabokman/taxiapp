from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import RegistrationView, LoginView,LogoutView

urlpatterns = [
    path('login/',LoginView.as_view(), name="login"),
    path('register/',RegistrationView.as_view(), name="register"),
    path('logout/',login_required(LogoutView.as_view(),login_url='/auth/login/'), name="logout"),
]
