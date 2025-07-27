from django.db import models
from django.urls import reverse # Added: Required for get_absolute_url
from django.utils import timezone # Added: Required for timezone.now
from django.contrib.auth.models import User # Assuming you're using Django's default User model for CustomUserCreationForm

# If you have a custom user model, you would import it like this instead:
# from .models import CustomUser # Assuming CustomUser is defined elsewhere in your models.py or a separate file

# Your existing Course model
class Course(models.Model):
    title = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    credits = models.IntegerField(default=3)
    department = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code}: {self.title}"

    # Optional: Define get_absolute_url if you want a detail view for courses
    def get_absolute_url(self):
        return reverse('course_detail', args=[str(self.pk)])

# Your existing Employee model
class Employee(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    hire_date = models.DateField()
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.position})"

    class Meta:
        ordering = ['last_name', 'first_name']

# Your existing Leave model
class Leave(models.Model):
    LEAVE_TYPES = [
        ('Annual', 'Annual Leave'),
        ('Sick', 'Sick Leave'),
        ('Maternity', 'Maternity Leave'),
        ('Paternity', 'Paternity Leave'),
        ('Compassionate', 'Compassionate Leave'),
        ('Study', 'Study Leave'),
        ('Unpaid', 'Unpaid Leave'),
        ('Other', 'Other'),
    ]

    LEAVE_STATUS = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Cancelled', 'Cancelled'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leaves')
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=LEAVE_STATUS, default='Pending')
    request_date = models.DateTimeField(auto_now_add=True) # Automatically set when created
    approved_by = models.CharField(max_length=100, blank=True, null=True) # E.g., name of approver
    approval_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name} - {self.leave_type} ({self.status})"

    @property
    def duration_days(self):
        """Calculates the duration of the leave in days."""
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days + 1
        return 0

    class Meta:
        ordering = ['-request_date'] # Order by most recent leave requests first
        verbose_name_plural = "Leaves" # Correct plural for "Leave" in admin


# NEW: Payroll Model
class Payroll(models.Model):
    employee = models.ForeignKey(
        'Employee',
        on_delete=models.CASCADE,
        related_name='payrolls',
        help_text="The employee associated with this payroll record."
    )
    pay_period_start = models.DateField(
        help_text="The start date of the pay period."
    )
    pay_period_end = models.DateField(
        help_text="The end date of the pay period."
    )
    gross_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Total earnings before deductions."
    )
    deductions = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Total deductions (e.g., taxes, benefits)."
    )
    net_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Earnings after all deductions."
    )
    date_processed = models.DateTimeField(
        default=timezone.now,
        help_text="The date and time this payroll was processed."
    )
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Any additional notes about this payroll."
    )

    class Meta:
        ordering = ['-pay_period_end', 'employee__last_name', 'employee__first_name']
        verbose_name = "Payroll Record"
        verbose_name_plural = "Payroll Records"
        unique_together = ('employee', 'pay_period_start', 'pay_period_end')

    def save(self, *args, **kwargs):
        # Automatically calculate net_salary before saving
        self.net_salary = self.gross_salary - self.deductions
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('payroll_detail', args=[str(self.id)])

    def __str__(self):
        return f"Payroll for {self.employee} ({self.pay_period_start} to {self.pay_period_end})"


# NEW: Student Model
class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    student_id = models.CharField(max_length=20, unique=True,
                                  help_text="Unique identifier for the student (e.g., matriculation number).")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    enrollment_date = models.DateField(default=timezone.now,
                                       help_text="The date the student enrolled in the university.")
    major = models.CharField(max_length=100, blank=True, null=True,
                             help_text="The student's primary field of study.")
    current_year = models.IntegerField(default=1,
                                       help_text="The current academic year the student is in (e.g., 1 for Freshmore, 4 for Senior).")
    is_active = models.BooleanField(default=True,
                                    help_text="Designates whether the student record is active.")

    class Meta:
        ordering = ['last_name', 'first_name', 'student_id']
        verbose_name = "Student"
        verbose_name_plural = "Students"

    def get_absolute_url(self):
        return reverse('student_detail', args=[str(self.pk)])

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"
