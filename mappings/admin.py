from django.contrib import admin
from .models import PatientDoctorMapping


@admin.register(PatientDoctorMapping)
class PatientDoctorMappingAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'status', 'assigned_date', 'created_by']
    list_filter = ['status', 'assigned_date', 'created_by']
    search_fields = ['patient__first_name', 'patient__last_name', 'doctor__first_name', 'doctor__last_name']
    readonly_fields = ['assigned_date', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Mapping Information', {
            'fields': ('patient', 'doctor', 'status', 'notes')
        }),
        ('System Information', {
            'fields': ('created_by', 'assigned_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
