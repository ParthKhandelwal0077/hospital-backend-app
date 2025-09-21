from django.contrib import admin
from .models import Doctor


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'specialization', 'license_number', 'years_of_experience', 
                   'is_available', 'created_by', 'created_at']
    list_filter = ['specialization', 'is_available', 'created_at', 'created_by']
    search_fields = ['first_name', 'last_name', 'email', 'license_number', 'clinic_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number')
        }),
        ('Professional Information', {
            'fields': ('specialization', 'license_number', 'years_of_experience', 
                      'qualification', 'consultation_fee', 'is_available')
        }),
        ('Clinic Information', {
            'fields': ('clinic_name', 'clinic_address', 'city', 'state', 'zip_code')
        }),
        ('System Information', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
