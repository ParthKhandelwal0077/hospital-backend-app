from rest_framework import serializers
from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Doctor
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'email', 'phone_number',
            'specialization', 'license_number', 'years_of_experience', 'qualification',
            'clinic_name', 'clinic_address', 'city', 'state', 'zip_code',
            'consultation_fee', 'is_available', 'created_by_username',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'full_name', 'created_by_username']

    def validate_email(self, value):
        """Ensure email is unique"""
        if self.instance:
            # If updating, exclude current instance from uniqueness check
            if Doctor.objects.exclude(pk=self.instance.pk).filter(email=value).exists():
                raise serializers.ValidationError("A doctor with this email already exists.")
        else:
            # If creating, check for any existing doctor with this email
            if Doctor.objects.filter(email=value).exists():
                raise serializers.ValidationError("A doctor with this email already exists.")
        return value

    def validate_license_number(self, value):
        """Ensure license number is unique"""
        if self.instance:
            # If updating, exclude current instance from uniqueness check
            if Doctor.objects.exclude(pk=self.instance.pk).filter(license_number=value).exists():
                raise serializers.ValidationError("A doctor with this license number already exists.")
        else:
            # If creating, check for any existing doctor with this license number
            if Doctor.objects.filter(license_number=value).exists():
                raise serializers.ValidationError("A doctor with this license number already exists.")
        return value


class DoctorCreateSerializer(DoctorSerializer):
    class Meta(DoctorSerializer.Meta):
        fields = [
            'first_name', 'last_name', 'email', 'phone_number',
            'specialization', 'license_number', 'years_of_experience', 'qualification',
            'clinic_name', 'clinic_address', 'city', 'state', 'zip_code',
            'consultation_fee', 'is_available'
        ]


class DoctorListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing doctors (public view)"""
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Doctor
        fields = [
            'id', 'full_name', 'specialization', 'years_of_experience',
            'qualification', 'clinic_name', 'city', 'state',
            'consultation_fee', 'is_available'
        ]
