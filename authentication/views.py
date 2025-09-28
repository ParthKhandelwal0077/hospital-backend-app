from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, BlacklistedToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer
import logging

logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        logger.info(f"Registration attempt - Request data: {request.data}")
        logger.info(f"Registration attempt - Request headers: {dict(request.headers)}")
        logger.info(f"Registration attempt - Content type: {request.content_type}")
        
        try:
            serializer = self.get_serializer(data=request.data)
            logger.info(f"Serializer created successfully")
            
            if serializer.is_valid():
                logger.info(f"Serializer validation successful")
                logger.info(f"Validated data: {serializer.validated_data}")
                
                user = serializer.save()
                logger.info(f"User created successfully: {user.username} (ID: {user.id})")
                
                refresh = RefreshToken.for_user(user)
                logger.info(f"JWT tokens generated for user: {user.username}")
                
                response_data = {
                    'message': 'User registered successfully',
                    'user': UserSerializer(user).data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }
                logger.info(f"Registration successful for user: {user.username}")
                
                response = Response(response_data, status=status.HTTP_201_CREATED)
                response['Content-Type'] = 'application/json'
                return response
            else:
                logger.error(f"Serializer validation failed")
                logger.error(f"Serializer errors: {serializer.errors}")
                
                # Log individual field errors
                for field, errors in serializer.errors.items():
                    logger.error(f"Field '{field}' errors: {errors}")
                
                # Log non-field errors if they exist
                if 'non_field_errors' in serializer.errors:
                    logger.error(f"Non-field errors: {serializer.errors['non_field_errors']}")
                
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            logger.error(f"Unexpected error during registration: {str(e)}")
            logger.error(f"Exception type: {type(e).__name__}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            
            return Response({
                'error': 'Internal server error during registration',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """API login endpoint - returns user data and JWT tokens"""
    logger.info(f"Login attempt for: {request.data.get('username', 'unknown')}")
    
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        
        logger.info(f"Login successful for user: {user.username}")
        
        response_data = {
            'message': 'Login successful',
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }
        
        response = Response(response_data, status=status.HTTP_200_OK)
        response['Content-Type'] = 'application/json'
        return response
    
    logger.warning(f"Login failed for: {request.data.get('username', 'unknown')} - {serializer.errors}")
    return Response({
        'error': 'Invalid credentials',
        'details': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile_view(request):
    """API endpoint to get current user profile"""
    logger.info(f"Profile request for user: {request.user.username}")
    
    serializer = UserSerializer(request.user)
    response_data = {
        'message': 'Profile retrieved successfully',
        'user': serializer.data
    }
    
    response = Response(response_data, status=status.HTTP_200_OK)
    response['Content-Type'] = 'application/json'
    return response


@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """API logout endpoint - blacklists the refresh token"""
    logger.info(f"Logout request for user: {request.user.username}")
    
    try:
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            logger.info(f"Logout successful for user: {request.user.username}")
            response_data = {
                'message': 'Logout successful',
                'user': request.user.username
            }
            
            response = Response(response_data, status=status.HTTP_200_OK)
            response['Content-Type'] = 'application/json'
            return response
        else:
            logger.warning(f"Logout failed for user {request.user.username}: No refresh token provided")
            return Response({
                'error': 'Refresh token is required'
            }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Logout error for user {request.user.username}: {str(e)}")
        return Response({
            'error': 'Invalid token or logout failed',
            'details': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
