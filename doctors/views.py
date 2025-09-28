from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
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
    
    def perform_create(self, serializer):
        """Set the created_by field to the current user"""
        serializer.save(created_by=self.request.user)
    
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
    """Retrieve doctor details"""
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