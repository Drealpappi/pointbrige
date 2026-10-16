from django.urls import path, include
from .views import RegisterView, LoginView, PasswordResetRequestView, home
from .views import TestAuthView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='token_obtain_pair'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('forgot_password/', PasswordResetRequestView.as_view(), name='forgot_password'),
    path('test/', TestAuthView.as_view()),
    path('home/', home, name='home'),
    path('dashboard/', home, name='dashboard'),
    path('api/', include('transactions.urls')),
]