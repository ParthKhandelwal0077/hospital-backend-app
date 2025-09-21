from django.db import models
from django.contrib.auth.models import User
from patients.models import Patient
from doctors.models import Doctor


class PatientDoctorMapping(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('COMPLETED', 'Completed'),
    ]
    
    # Relationships
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='doctor_mappings')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='patient_mappings')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mappings')
    
    # Mapping details
    assigned_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    notes = models.TextField(blank=True, help_text="Additional notes about the patient-doctor assignment")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['patient', 'doctor']  # Prevent duplicate assignments
        
    def __str__(self):
        return f"{self.patient.full_name} -> {self.doctor.full_name}"
