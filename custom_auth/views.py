import os
from django.shortcuts import render
from rest_framework.authtoken.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.conf import settings
from django.shortcuts import redirect
from custom_auth.serializers import UserSerializer, LoginSerializer
from django.utils.http import urlsafe_base64_decode
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.tokens import default_token_generator as token_generator, PasswordResetTokenGenerator
from .models import User, PasswordReset
from django.http import HttpResponse
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from .models import User
from .serializers import ResetPasswordRequestSerializer




class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to the login endpoint.

        Validate the provided email and password using the LoginSerializer.
        If the credentials are correct, return a JSON response with the user's
        authentication token and serialized user data.

        If the credentials are invalid, return a 400 Bad Request response with
        the serializer's validation errors.
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user': UserSerializer(user).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignupView(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = []

    def create(self, request):
        """
        Handle POST requests to the signup endpoint.

        Validate the provided user data using the UserSerializer.
        If the data is valid, save the user and return a JSON response with the
        serialized user data.

        If the data is invalid, return a 400 Bad Request response with the
        serializer's validation errors.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ActivateUserView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, uidb64, token):
        """
        Handle GET requests to the user activation endpoint.

        Validate the activation link using the token generator.
        If the link is valid, activate the user and return a success response.
        If the link is invalid, return an error response.

        Parameters:
        - request: The HTTP request object.
        - uidb64: The user's id encoded in base64.
        - token: The activation token.

        Returns:
        - A 200 OK response if the user is activated successfully.
        - A 400 Bad Request response if the activation link is invalid.
        """
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"message": "Your account has been activated successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Activation link is invalid or expired."}, status=status.HTTP_400_BAD_REQUEST)

class VerifyTokenView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Verify a token sent by the frontend is valid.

        The frontend token is compared with the user's token in the request's
        authentication header. If the two match, a 200 response is returned,
        indicating that the token is valid. If the two do not match, a 401
        response is returned, indicating that the token is not valid.

        :param request: The request object
        :return: A response with a status of 200 if the token is valid, 401 otherwise
        """
        frontend_token = request.data.get('token')
        user_token = request.auth
        
        if frontend_token == str(user_token):
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        
class PasswordResetView(APIView):
    permission_classes = []

    def get(self, request, token):
        """
        Check if the given token is valid and not expired.

        Args:
            request (Request): The request object.
            token (str): The token to check.

        Returns:
            Response: 200 with {'success': 'Token is valid'} if the token is valid and not expired.
            Response: 400 with {'error': 'Invalid token'} if the token is not valid.
            Response: 400 with {'error': 'Token expired'} if the token is expired.
        """
        reset_obj = PasswordReset.objects.filter(token=token).first()
        if not reset_obj:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        token_lifetime = timedelta(hours=24)
        if timezone.now() > reset_obj.created_at + token_lifetime:
            return Response({'error': 'Token expired'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'success': 'Token is valid'}, status=status.HTTP_200_OK)

    def post(self, request, token):
        """
        Resets the password for the given user

        Args:
            request: The request object
            token: The token from the password reset email

        Returns:
            A response object with a status code and a message
        """
        reset_obj = PasswordReset.objects.filter(token=token).first()
        if not reset_obj:
            return Response({'error': 'Invalid token'}, status=400)

        token_lifetime = timedelta(hours=24)
        if timezone.now() > reset_obj.created_at + token_lifetime:
            return Response({'error': 'Token expired'}, status=400)

        user = User.objects.filter(email=reset_obj.email).first()
        if user:
            user.set_password(request.data['password'])
            user.save()
            reset_obj.delete()
            return Response({'success': 'Password updated'})
        else:
            return Response({'error': 'No user found'}, status=404)
        
class RequestPasswordReset(APIView):
    permission_classes = [AllowAny]
    TokenAuthentication = [AllowAny]
    User = User
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request):
        """
        Handles the password reset request by generating a token and sending a reset email.

        Args:
            request: The request object containing the user's email.

        The function checks if a user with the provided email exists. If the user exists,
        it generates a password reset token, saves it, and sends an email to the user
        with a reset link. If the email is not found, a 404 response is returned.

        Returns:
            Response: A success message with a 200 status if the email is sent successfully.
            Response: An error message with a 404 status if the user is not found.
        """
        email = request.data['email']
        user = User.objects.filter(email__iexact=email).first()

        if user:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user) 
            reset = PasswordReset(email=email, token=token)
            reset.save()

            reset_url = reverse('password_reset_token', kwargs={'token': token})
            relative_reset_url = reset_url.replace('/videoflix', '')
            custom_port_url = os.getenv('REDIRECT_LANDING') + relative_reset_url
            full_url = custom_port_url
            domain_url = os.getenv('REDIRECT_LANDING')
            subject = "Reset your password"
            text_content = render_to_string('emails/forgot_password.txt', {
                'username': user.username, 
                'full_url': full_url,
                'domain_url': domain_url,
            })
            html_content = render_to_string('emails/forgot_password.html', {
                'username': user.username, 
                'full_url': full_url,
                'domain_url': domain_url,
            })
            email = EmailMultiAlternatives(
                subject,
                text_content,
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )
            email.attach_alternative(html_content, "text/html")
            email.send()
            return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)