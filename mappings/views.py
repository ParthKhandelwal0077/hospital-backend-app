from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from .models import PatientDoctorMapping
from patients.models import Patient
from .serializers import (
    PatientDoctorMappingSerializer, 
    PatientDoctorMappingCreateSerializer,
    PatientMappingsSerializer
)


class MappingListCreateView(generics.ListCreateAPIView):
    """List all mappings or create a new patient-doctor mapping"""
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PatientDoctorMappingCreateSerializer
        return PatientDoctorMappingSerializer
    
    def get_queryset(self):
        """Return mappings created by the authenticated user"""
        return PatientDoctorMapping.objects.filter(created_by=self.request.user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            mapping = serializer.save(created_by=request.user)
            return Response({
                'message': 'Patient assigned to doctor successfully',
                'mapping': PatientDoctorMappingSerializer(mapping).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MappingDeleteView(generics.DestroyAPIView):
    """Remove a doctor from a patient"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return mappings created by the authenticated user"""
        return PatientDoctorMapping.objects.filter(created_by=self.request.user)
    
    def get_object(self):
        """Get mapping by ID, ensuring it belongs to the authenticated user"""
        queryset = self.get_queryset()
        mapping_id = self.kwargs.get('pk')
        return get_object_or_404(queryset, pk=mapping_id)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        patient_name = instance.patient.full_name
        doctor_name = instance.doctor.full_name
        instance.delete()
        return Response({
            'message': f'Successfully removed {doctor_name} from {patient_name}'
        }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def patient_doctors_view(request, patient_id):
    """Get all doctors assigned to a specific patient"""
    # Ensure the patient belongs to the current user
    patient = get_object_or_404(
        Patient.objects.filter(created_by=request.user), 
        pk=patient_id
    )
    
    # Get all active mappings for this patient
    mappings = PatientDoctorMapping.objects.filter(
        patient=patient,
        created_by=request.user
    )
    
    serializer = PatientMappingsSerializer(mappings, many=True)
    return Response({
        'patient': {
            'id': patient.id,
            'name': patient.full_name,
            'email': patient.email
        },
        'doctors': serializer.data
    }, status=status.HTTP_200_OK)


class MappingUpdateView(generics.UpdateAPIView):
    """Update mapping status or notes"""
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Return mappings created by the authenticated user"""
        return PatientDoctorMapping.objects.filter(created_by=self.request.user)
    
    def get_object(self):
        """Get mapping by ID, ensuring it belongs to the authenticated user"""
        queryset = self.get_queryset()
        mapping_id = self.kwargs.get('pk')
        return get_object_or_404(queryset, pk=mapping_id)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            mapping = serializer.save()
            return Response({
                'message': 'Mapping updated successfully',
                'mapping': PatientDoctorMappingSerializer(mapping).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
