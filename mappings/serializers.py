from rest_framework import serializers
from .models import PatientDoctorMapping
from patients.models import Patient
from doctors.models import Doctor


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.full_name', read_only=True)
    doctor_specialization = serializers.CharField(source='doctor.specialization', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = [
            'id', 'patient', 'doctor', 'patient_name', 'doctor_name', 
            'doctor_specialization', 'assigned_date', 'status', 'notes',
            'created_by_username', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'assigned_date', 'created_at', 'updated_at', 
                           'patient_name', 'doctor_name', 'doctor_specialization', 
                           'created_by_username']

    def validate(self, attrs):
        patient = attrs.get('patient')
        doctor = attrs.get('doctor')
        request = self.context.get('request')
        
        # Ensure patient belongs to the current user
        if patient and patient.created_by != request.user:
            raise serializers.ValidationError("You can only assign your own patients to doctors.")
        
        # Check if mapping already exists (for create operation)
        if not self.instance and PatientDoctorMapping.objects.filter(
            patient=patient, doctor=doctor
        ).exists():
            raise serializers.ValidationError("This patient is already assigned to this doctor.")
        
        return attrs


class PatientDoctorMappingCreateSerializer(PatientDoctorMappingSerializer):
    class Meta(PatientDoctorMappingSerializer.Meta):
        fields = ['patient', 'doctor', 'status', 'notes']

    def validate_patient(self, value):
        """Ensure the patient belongs to the current user"""
        request = self.context.get('request')
        if value.created_by != request.user:
            raise serializers.ValidationError("You can only assign your own patients.")
        return value


class PatientMappingsSerializer(serializers.ModelSerializer):
    """Serializer for getting all doctors assigned to a specific patient"""
    doctor_name = serializers.CharField(source='doctor.full_name', read_only=True)
    doctor_specialization = serializers.CharField(source='doctor.specialization', read_only=True)
    doctor_clinic = serializers.CharField(source='doctor.clinic_name', read_only=True)
    doctor_phone = serializers.CharField(source='doctor.phone_number', read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = [
            'id', 'doctor', 'doctor_name', 'doctor_specialization', 
            'doctor_clinic', 'doctor_phone', 'assigned_date', 'status', 'notes'
        ]
