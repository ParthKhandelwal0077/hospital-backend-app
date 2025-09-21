from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from patients.models import Patient
from doctors.models import Doctor
from mappings.models import PatientDoctorMapping


# Home and Dashboard Views
def home_view(request):
    """Home page view"""
    return render(request, 'home.html')


@login_required
def dashboard_view(request):
    """Dashboard view with statistics"""
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
    
    return render(request, 'dashboard.html', context)


# Authentication Views
def register_view(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Set additional user fields
            user.first_name = request.POST.get('first_name', '')
            user.last_name = request.POST.get('last_name', '')
            user.email = request.POST.get('email', '')
            user.save()
            
            # Log in the user
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    
    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    """User login view"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'auth/login.html')


@login_required
def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required
def profile_view(request):
    """User profile view"""
    return render(request, 'auth/profile.html')


# Patient Views
class PatientListView(LoginRequiredMixin, ListView):
    """Patient list view with search and filtering"""
    model = Patient
    template_name = 'patients/list.html'
    context_object_name = 'patients'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Patient.objects.filter(created_by=self.request.user)
        
        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(phone_number__icontains=search)
            )
        
        # Filter by gender
        gender = self.request.GET.get('gender')
        if gender:
            queryset = queryset.filter(gender=gender)
        
        # Filter by city
        city = self.request.GET.get('city')
        if city:
            queryset = queryset.filter(city__icontains=city)
        
        # Filter by blood type
        blood_type = self.request.GET.get('blood_type')
        if blood_type:
            queryset = queryset.filter(blood_type__icontains=blood_type)
        
        return queryset.order_by('-created_at')


class PatientDetailView(LoginRequiredMixin, DetailView):
    """Patient detail view"""
    model = Patient
    template_name = 'patients/detail.html'
    context_object_name = 'patient'
    
    def get_queryset(self):
        return Patient.objects.filter(created_by=self.request.user)


# Doctor Views
class DoctorListView(LoginRequiredMixin, ListView):
    """Doctor list view"""
    model = Doctor
    template_name = 'doctors/list.html'
    context_object_name = 'doctors'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Doctor.objects.all()  # All doctors are visible
        
        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(specialization__icontains=search) |
                Q(clinic_name__icontains=search)
            )
        
        # Filter by specialization
        specialization = self.request.GET.get('specialization')
        if specialization:
            queryset = queryset.filter(specialization=specialization)
        
        # Filter by availability
        available = self.request.GET.get('available')
        if available == 'true':
            queryset = queryset.filter(is_available=True)
        elif available == 'false':
            queryset = queryset.filter(is_available=False)
        
        return queryset.order_by('-created_at')


class DoctorDetailView(LoginRequiredMixin, DetailView):
    """Doctor detail view"""
    model = Doctor
    template_name = 'doctors/detail.html'
    context_object_name = 'doctor'


# Mapping Views
class MappingListView(LoginRequiredMixin, ListView):
    """Patient-Doctor mapping list view"""
    model = PatientDoctorMapping
    template_name = 'mappings/list.html'
    context_object_name = 'mappings'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = PatientDoctorMapping.objects.filter(created_by=self.request.user)
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset.order_by('-created_at')


# API Test View
@login_required
def api_test_view(request):
    """API testing interface"""
    return render(request, 'api_test.html')
