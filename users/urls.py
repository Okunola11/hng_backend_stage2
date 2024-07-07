from django.urls import path
from .views import RegisterView, LoginView, UserDetailView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path('api/users/<str:user_id>/', UserDetailView.as_view(), name='user-detail'),

]
