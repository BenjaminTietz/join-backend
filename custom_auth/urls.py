# auth/urls.py
from django.urls import path
from .views import LoginView, SignupView, ActivateUserView, VerifyTokenView, RequestPasswordReset, PasswordResetView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view({'post': 'create'}), name='signup'),
    path('activate/<uidb64>/<token>/', ActivateUserView.as_view(), name='activate_user'),
    path('password-reset/', RequestPasswordReset.as_view(), name='password_reset'),
    path('password-reset/<token>/', PasswordResetView.as_view(), name='password_reset_token'),
    path('verify-token/', VerifyTokenView.as_view(), name='verify_token'),
]
