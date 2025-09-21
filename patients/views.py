from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
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
