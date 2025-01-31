from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.utils.http import urlsafe_base64_decode
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from .models import User
import os

def activate_user(request, uidb64, token):
    """
    Activate a user's account given an activation link.

    The function validates the activation link and if valid, activates the user's
    account. If the account is already activated, it displays a success message.
    If the link is invalid, it displays an error message.

    Parameters:
    - request: Django's request object.
    - uidb64: The user's id encoded in base64.
    - token: The activation token.

    Returns:
    - A redirect to the login page if the account is activated or already active.
    - A redirect to the landing page if the link is invalid.
    """
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and token_generator.check_token(user, token):
        if not user.is_active: 
            user.is_active = True
            user.save()
            messages.success(request, 'Your account has been activated.')
        else:
            messages.info(request, 'Your account is already activated.')
        return redirect(os.getenv('REDIRECT_LOGIN'))
    else:
        messages.error(request, 'The activation link is invalid!')
        return redirect(os.getenv('REDIRECT_LANDING'))