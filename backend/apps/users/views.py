import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from django.db import connection

from .models import Business
from .serializers import (
    SignupSerializer, 
    LoginSerializer, 
    BusinessSerializer,
    UserSerializer,
    PasswordChangeSerializer,
)

logger = logging.getLogger(__name__)
User = get_user_model()


class HealthCheckView(APIView):
    """Health check endpoint for container orchestration"""
    permission_classes = [AllowAny]
    
    def get(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            db_status = "healthy"
        except Exception as e:
            db_status = f"unhealthy: {str(e)}"
            logger.error(f"Health check failed: {e}")
            return Response({
                "status": "unhealthy",
                "database": db_status
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
        return Response({
            "status": "healthy",
            "database": db_status
        })


class SignupView(APIView):
    """User registration endpoint"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        
        if not serializer.is_valid():
            logger.warning(f"Signup validation failed: {serializer.errors}")
            return Response({
                'success': False,
                'message': 'Validation failed. Please check your input.',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            data = serializer.save()
            user = data['user']
            business = data['business']
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            
            logger.info(f"User signup successful: {user.username}")
            
            return Response({
                'success': True,
                'message': 'Registration successful. Welcome!',
                'data': {
                    'user': UserSerializer(user).data,
                    'business': BusinessSerializer(business).data,
                    'tokens': {
                        'access': str(refresh.access_token),
                        'refresh': str(refresh)
                    }
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Signup error: {str(e)}")
            return Response({
                'success': False,
                'message': 'An error occurred during registration. Please try again.',
                'errors': {'general': str(e)}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    """User login endpoint with improved error handling"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if not serializer.is_valid():
            logger.warning(f"Login validation failed: {serializer.errors}")
            return Response({
                'success': False,
                'message': 'Validation failed. Please check your input.',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.validated_data.get('user')
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        # Try to authenticate with email
        if user is None:
            # Check if user exists
            if not User.objects.filter(email=email).exists():
                logger.warning(f"Login failed - user not found: {email}")
                return Response({
                    'success': False,
                    'message': 'Invalid email or password.',
                    'errors': {}
                }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Verify password
        if not user.check_password(password):
            logger.warning(f"Login failed - wrong password: {email}")
            return Response({
                'success': False,
                'message': 'Invalid email or password.',
                'errors': {}
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check if user is active
        if not user.is_active:
            logger.warning(f"Login failed - inactive user: {email}")
            return Response({
                'success': False,
                'message': 'Your account has been deactivated. Please contact support.',
                'errors': {}
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Get business
        try:
            business = user.business
        except Business.DoesNotExist:
            logger.warning(f"Login failed - no business found: {email}")
            # Create business if it doesn't exist
            business = Business.objects.create(
                owner=user,
                name=f"{user.username}'s Business",
                email=user.email
            )
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        logger.info(f"Login successful: {email}")
        
        return Response({
            'success': True,
            'message': 'Login successful. Welcome back!',
            'data': {
                'user': UserSerializer(user).data,
                'business': BusinessSerializer(business).data,
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
            }
        }, status=status.HTTP_200_OK)


class MeView(APIView):
    """Get current authenticated user and their business"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        try:
            business = user.business
            business_data = BusinessSerializer(business).data
        except Business.DoesNotExist:
            business_data = None
        
        return Response({
            'success': True,
            'message': 'User retrieved successfully.',
            'data': {
                'user': UserSerializer(user).data,
                'business': business_data
            }
        })


class BusinessDetailView(APIView):
    """Get and update business details"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            business = request.user.business
            serializer = BusinessSerializer(business)
            return Response({
                'success': True,
                'data': serializer.data
            })
        except Business.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Business not found.',
                'errors': {}
            }, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        try:
            business = request.user.business
            serializer = BusinessSerializer(business, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'success': True,
                    'message': 'Business updated successfully.',
                    'data': serializer.data
                })
            
            return Response({
                'success': False,
                'message': 'Validation failed.',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Business.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Business not found.',
                'errors': {}
            }, status=status.HTTP_404_NOT_FOUND)


class PasswordChangeView(APIView):
    """Change user password"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                'success': False,
                'message': 'Validation failed.',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = request.user
        
        # Verify current password
        if not user.check_password(serializer.validated_data['current_password']):
            return Response({
                'success': False,
                'message': 'Current password is incorrect.',
                'errors': {'current_password': 'Current password is incorrect.'}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Set new password
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        logger.info(f"Password changed successfully for user: {user.username}")
        
        return Response({
            'success': True,
            'message': 'Password changed successfully.'
        })


class LogoutView(APIView):
    """User logout (token blacklist)"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            logger.info(f"User logged out: {request.user.username}")
            
            return Response({
                'success': True,
                'message': 'Logged out successfully.'
            })
        except Exception as e:
            logger.warning(f"Logout error: {str(e)}")
            return Response({
                'success': True,
                'message': 'Logged out.'
            })
