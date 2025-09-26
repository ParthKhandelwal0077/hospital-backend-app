from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Patient
from .serializers import PatientSerializer, PatientCreateSerializer


class PatientListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PatientCreateSerializer
        return PatientSerializer
    
    def get_queryset(self):
        """Return patients created by the authenticated user"""
        return Patient.objects.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        """Set the created_by field to the current user"""
        serializer.save(created_by=self.request.user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            patient = serializer.save(created_by=request.user)
            return Response({
                'message': 'Patient created successfully',
                'patient': PatientSerializer(patient).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return patients created by the authenticated user"""
        return Patient.objects.filter(created_by=self.request.user)
    
    def get_object(self):
        """Get patient by ID, ensuring it belongs to the authenticated user"""
        queryset = self.get_queryset()
        patient_id = self.kwargs.get('pk')
        return get_object_or_404(queryset, pk=patient_id)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            patient = serializer.save()
            return Response({
                'message': 'Patient updated successfully',
                'patient': PatientSerializer(patient).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({
            'message': 'Patient deleted successfully'
        }, status=status.HTTP_200_OK)


# Simple Web Views
@login_required
def patient_list_view(request):
    """Simple patient list view"""
    queryset = Patient.objects.filter(created_by=request.user)
    
    # Search functionality
    search = request.GET.get('search')
    if search:
        queryset = queryset.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone_number__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(queryset.order_by('-created_at'), 10)
    page_number = request.GET.get('page')
    patients = paginator.get_page(page_number)
    
    return render(request, 'simple_patient_list.html', {
        'patients': patients,
        'search': search
    })


@login_required
def patient_create_view(request):
    """Simple patient creation"""
    error_message = None
    success_message = None
    
    if request.method == 'POST':
        try:
            # Get form data
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            phone_number = request.POST.get('phone_number')
            date_of_birth = request.POST.get('date_of_birth')
            gender = request.POST.get('gender')
            address = request.POST.get('address', '')
            city = request.POST.get('city', '')
            state = request.POST.get('state', '')
            zip_code = request.POST.get('zip_code', '')
            
            # Basic validation
            if not all([first_name, last_name, email, phone_number, date_of_birth, gender]):
                error_message = "All required fields must be filled"
            elif Patient.objects.filter(email=email).exists():
                error_message = "A patient with this email already exists"
            else:
                # Create patient
                patient = Patient.objects.create(
                    created_by=request.user,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    phone_number=phone_number,
                    date_of_birth=date_of_birth,
                    gender=gender,
                    address=address,
                    city=city,
                    state=state,
                    zip_code=zip_code
                )
                return redirect('patient_list')
                
        except Exception as e:
            error_message = f"Error creating patient: {str(e)}"
    
    return render(request, 'simple_patient_create.html', {
        'error': error_message,
        'success': success_message
    })
