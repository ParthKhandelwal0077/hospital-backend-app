from rest_framework import serializers
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Patient
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'email', 'phone_number',
            'date_of_birth', 'gender', 'address', 'city', 'state', 'zip_code',
            'blood_type', 'allergies', 'medical_history', 'created_by_username',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_email(self, value):
        """Ensure email is unique"""
        if self.instance:
            # If updating, exclude current instance from uniqueness check
            if Patient.objects.exclude(pk=self.instance.pk).filter(email=value).exists():
                raise serializers.ValidationError("A patient with this email already exists.")
        else:
            # If creating, check for any existing patient with this email
            if Patient.objects.filter(email=value).exists():
                raise serializers.ValidationError("A patient with this email already exists.")
        return value


class PatientCreateSerializer(PatientSerializer):
    class Meta(PatientSerializer.Meta):
        fields = [
            'first_name', 'last_name', 'email', 'phone_number',
            'date_of_birth', 'gender', 'address', 'city', 'state', 'zip_code',
            'blood_type', 'allergies', 'medical_history'
        ]
