from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Doctor
from .serializers import DoctorSerializer, DoctorCreateSerializer, DoctorListSerializer


class DoctorListView(generics.ListAPIView):
    """Public view to list all available doctors"""
    queryset = Doctor.objects.filter(is_available=True)
    serializer_class = DoctorListSerializer
    permission_classes = [IsAuthenticated]


class DoctorCreateView(generics.CreateAPIView):
    """Create a new doctor (authenticated users only)"""
    serializer_class = DoctorCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            doctor = serializer.save(created_by=request.user)
            return Response({
                'message': 'Doctor created successfully',
                'doctor': DoctorSerializer(doctor).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorRetrieveView(generics.RetrieveAPIView):
    """Get details of a specific doctor"""
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]


class DoctorUpdateView(generics.UpdateAPIView):
    """Update doctor details (only by the user who created the doctor)"""
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return doctors created by the authenticated user"""
        return Doctor.objects.filter(created_by=self.request.user)
    
    def get_object(self):
        """Get doctor by ID, ensuring it belongs to the authenticated user"""
        queryset = self.get_queryset()
        doctor_id = self.kwargs.get('pk')
        return get_object_or_404(queryset, pk=doctor_id)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            doctor = serializer.save()
            return Response({
                'message': 'Doctor updated successfully',
                'doctor': DoctorSerializer(doctor).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorDeleteView(generics.DestroyAPIView):
    """Delete doctor (only by the user who created the doctor)"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return doctors created by the authenticated user"""
        return Doctor.objects.filter(created_by=self.request.user)
    
    def get_object(self):
        """Get doctor by ID, ensuring it belongs to the authenticated user"""
        queryset = self.get_queryset()
        doctor_id = self.kwargs.get('pk')
        return get_object_or_404(queryset, pk=doctor_id)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({
            'message': 'Doctor deleted successfully'
        }, status=status.HTTP_200_OK)


# Simple Web Views
@login_required
def doctor_list_view(request):
    """Simple doctor list view"""
    queryset = Doctor.objects.all()  # All doctors are visible
    
    # Search functionality
    search = request.GET.get('search')
    if search:
        queryset = queryset.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(specialization__icontains=search) |
            Q(clinic_name__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(queryset.order_by('-created_at'), 10)
    page_number = request.GET.get('page')
    doctors = paginator.get_page(page_number)
    
    return render(request, 'simple_doctor_list.html', {
        'doctors': doctors,
        'search': search
    })


@login_required
def doctor_create_view(request):
    """Simple doctor creation"""
    error_message = None
    success_message = None
    
    if request.method == 'POST':
        try:
            # Get form data
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            specialization = request.POST.get('specialization')
            years_of_experience = request.POST.get('years_of_experience', 0)
            clinic_name = request.POST.get('clinic_name', '')
            clinic_address = request.POST.get('clinic_address', '')
            clinic_city = request.POST.get('clinic_city', '')
            clinic_state = request.POST.get('clinic_state', '')
            clinic_zip_code = request.POST.get('clinic_zip_code', '')
            
            # Basic validation
            if not all([first_name, last_name, email, phone_number, specialization]):
                error_message = "All required fields must be filled"
            elif Doctor.objects.filter(email=email).exists():
                error_message = "A doctor with this email already exists"
            else:
                # Create doctor
                doctor = Doctor.objects.create(
                    created_by=request.user,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone_number=phone_number,
                    specialization=specialization,
                    years_of_experience=int(years_of_experience) if years_of_experience else 0,
                    clinic_name=clinic_name,
                    clinic_address=clinic_address,
                    clinic_city=clinic_city,
                    clinic_state=clinic_state,
                    clinic_zip_code=clinic_zip_code
                )
                return redirect('doctor_list')
                
        except Exception as e:
            error_message = f"Error creating doctor: {str(e)}"
    
    return render(request, 'simple_doctor_create.html', {
        'error': error_message,
        'success': success_message
    })
