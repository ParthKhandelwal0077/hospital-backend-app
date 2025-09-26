from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'User registered successfully',
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'message': 'Login successful',
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile_view(request):
    serializer = UserSerializer(request.user)
    return Response({
        'user': serializer.data
    }, status=status.HTTP_200_OK)


# Web Views (Frontend)
def home_view(request):
    """Home page view"""
    return render(request, 'simple_home.html')


def web_register_view(request):
    """Simple user registration"""
    error_message = None
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        
        # Basic validation
        if not username or not password1 or not password2:
            error_message = "All fields are required"
        elif password1 != password2:
            error_message = "Passwords do not match"
        elif User.objects.filter(username=username).exists():
            error_message = "Username already exists"
        elif len(password1) < 4:
            error_message = "Password must be at least 4 characters"
        else:
            # Create user
            try:
                user = User.objects.create_user(
                    username=username,
                    password=password1,
                    email=email or ''
                )
                # Auto login
                login(request, user)
                return redirect('dashboard')
            except Exception as e:
                error_message = f"Error creating account: {str(e)}"
    
    return render(request, 'simple_register.html', {'error': error_message})


def web_login_view(request):
    """Simple user login"""
    error_message = None
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            error_message = "Username and password are required"
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                error_message = "Invalid username or password"
    
    return render(request, 'simple_login.html', {'error': error_message})


def web_logout_view(request):
    """Simple logout"""
    logout(request)
    return redirect('home')


@login_required
def dashboard_view(request):
    """Dashboard view with statistics"""
    from patients.models import Patient
    from doctors.models import Doctor
    from mappings.models import PatientDoctorMapping
    
    # Get user's data
    patients = Patient.objects.filter(created_by=request.user)
    doctors = Doctor.objects.filter(created_by=request.user)
    mappings = PatientDoctorMapping.objects.filter(created_by=request.user)
    
    # Recent items (last 5)
    recent_patients = patients.order_by('-created_at')[:5]
    recent_doctors = doctors.order_by('-created_at')[:5]
    recent_mappings = mappings.order_by('-created_at')[:5]
    
    context = {
        'patient_count': patients.count(),
        'doctor_count': doctors.count(),
        'mapping_count': mappings.filter(status='ACTIVE').count(),
        'recent_activities': mappings.count(),
        'recent_patients': recent_patients,
        'recent_doctors': recent_doctors,
        'recent_mappings': recent_mappings,
    }
    
    return render(request, 'simple_dashboard.html', context)
