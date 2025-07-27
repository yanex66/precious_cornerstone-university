# precious_cornerstone/UNIVERSITY/admin.py

from django.contrib import admin
# UPDATED: Import Student
from .models import Course, Employee, Leave, Payroll, Student

# ... (Your existing admin registrations for Course, Employee, Leave, Payroll) ...

# NEW: Register the Student model
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'email', 'major', 'current_year', 'is_active')
    list_filter = ('is_active', 'gender', 'major', 'current_year', 'enrollment_date')
    search_fields = ('first_name', 'last_name', 'student_id', 'email', 'major')
    date_hierarchy = 'enrollment_date'
    ordering = ('last_name', 'first_name')
    fieldsets = (
        (None, {
            'fields': (('first_name', 'last_name'), 'student_id', 'email', 'phone_number')
        }),
        ('Personal Information', {
            'fields': (('date_of_birth', 'gender'),)
        }),
        ('Academic Information', {
            'fields': ('enrollment_date', 'major', 'current_year', 'is_active')
        }),
    )