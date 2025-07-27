from django import forms
# Ensure all models you are creating forms for are imported
from .models import Employee, Leave, Payroll, Student # Student is here
from django.contrib.auth.forms import UserCreationForm
# You might be using a CustomUser model, or Django's built-in User.
# If CustomUser is defined in your models.py, import that instead of django.contrib.auth.models.User
from django.contrib.auth.models import User # Or from .models import CustomUser

# Your CustomUserCreationForm
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User # Or CustomUser if you defined it in .models
        fields = UserCreationForm.Meta.fields + ('email',)

# Your existing EmployeeForm
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        widgets = {
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

# Your existing LeaveForm
class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = '__all__'
        exclude = ['request_date', 'approved_by', 'approval_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'rows': 4}),
        }

# Your existing PayrollForm
class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = ['employee', 'pay_period_start', 'pay_period_end', 'gross_salary', 'deductions', 'notes']
        widgets = {
            'pay_period_start': forms.DateInput(attrs={'type': 'date'}),
            'pay_period_end': forms.DateInput(attrs={'type': 'date'}),
            'gross_salary': forms.NumberInput(attrs={'step': '0.01'}),
            'deductions': forms.NumberInput(attrs={'step': '0.01'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'pay_period_start': 'Pay Period Start Date',
            'pay_period_end': 'Pay Period End Date',
            'gross_salary': 'Gross Salary (₦)',
            'deductions': 'Total Deductions (₦)',
        }

# CORRECTED StudentForm - Removed 'address' as it's not in your Student model
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        # The 'address' field has been REMOVED from this list to match your Student model
        fields = ['student_id', 'first_name', 'last_name', 'date_of_birth', 'email', 'phone_number', 'major', 'enrollment_date', 'gender', 'current_year', 'is_active']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'enrollment_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'student_id': 'Student ID',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'date_of_birth': 'Date of Birth',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            # 'address': 'Residential Address', # This line should be commented out or removed if it was here
            'major': 'Major Subject',
            'enrollment_date': 'Enrollment Date',
            'gender': 'Gender',
            'current_year': 'Current Academic Year',
            'is_active': 'Is Active Student',
        }