from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import (
    HealthCheckView,
    SignupView,
    LoginView,
    MeView,
    BusinessDetailView,
    PasswordChangeView,
    LogoutView,
)

urlpatterns = [
    # Health check
    path('health/', HealthCheckView.as_view(), name='health-check'),
    
    # Authentication
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', MeView.as_view(), name='me'),
    
    # Business
    path('business/', BusinessDetailView.as_view(), name='business-detail'),
    
    # Password
    path('password-change/', PasswordChangeView.as_view(), name='password-change'),
    
    # JWT Token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
