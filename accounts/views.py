from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer, PasswordResetRequestSerializer
from django.contrib.auth import authenticate, login
from wallets.models import Wallet
from transactions.models import Wallet
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator

User = get_user_model()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'User registered successfully!!'
            }, status=status.HTTP_201_CREATED)

        # In cse of Validation failed — This will return errors to the frontend side
        return Response({
            'success': False,
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, 'login.html')
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)

            return Response(
                {
                    'success': True,
                    'message': "Logged in successfuly"
                }, status=status.HTTP_200_OK
            )
        
        else:
            return Response(
                {
                    'success': False,
                    'error': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST
        )

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request):

        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Profile updated successfully",
                    "data": serializer.data
                }, status=status.HTTP_200_OK
            )
        
        return Response(
            {
                "success": False,
                "error": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST
        )

class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, 'forgot_password.html')

    def post (self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        user = User.objects.filter(email=email).first()
        if user:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = f"/api/account/reset-password/?uid={uidb64}&token={token}"
            # Email delivery can be connected here once the project's email backend is configured.

        return Response({
            'success': True,
            'message': 'If an account exists for that email, a password reset link has been sent.'
        }, status=status.HTTP_200_OK)

class TestAuthView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "message": "You are authenticated"
        })

@login_required(login_url='api/account/login/')
def home(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    return render(request, 'home.html', {'wallet': wallet})