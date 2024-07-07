from django.urls import path
from .views import RegisterView, LoginView, UserDetailView

urlpatterns = [
    path('auth/register', RegisterView.as_view(), name='auth-register'),
    path('auth/login', LoginView.as_view(), name='auth-login'),
    path('api/users/<str:userId>', UserDetailView.as_view(), name='user-detail'),

]
