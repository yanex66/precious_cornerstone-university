# precious_cornerstone/UNIVERSITY/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Course, Employee, Leave, Payroll, Student # Ensure Student model is imported
from .forms import EmployeeForm, LeaveForm, PayrollForm, CustomUserCreationForm, StudentForm

from django.utils import timezone
from django.db.models import Q # Import Q object for complex lookups

# Existing views
def index(request):
    context = {
        'university_name': 'Precious Cornerstone University',
        'current_year': timezone.now().year
    }
    return render(request, 'UNIVERSITY/index.html', context)

# NEW: Registration view
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# --- Course Management Views (NOW CLASS-BASED) ---
@method_decorator(login_required, name='dispatch')
class CourseListView(ListView):
    model = Course
    template_name = 'UNIVERSITY/course_list.html'
    context_object_name = 'courses'
    ordering = ['code'] # Order by course code as in your original function view

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['university_name'] = 'Precious Cornerstone University'
        # Pass the query back to the template for the search bar
        context['query'] = self.request.GET.get('q', '')
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(code__icontains=query) |
                Q(title__icontains=query) |
                Q(department__icontains=query)
            ).distinct()
        return queryset


@method_decorator(login_required, name='dispatch')
class CourseDetailView(DetailView):
    model = Course
    template_name = 'UNIVERSITY/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['university_name'] = 'Precious Cornerstone University'
        return context

# --- Employee Management Views ---

def employee_list(request):
    employees = Employee.objects.all()
    context = {
        'employees': employees,
        'university_name': 'Precious Cornerstone University'
    }
    return render(request, 'UNIVERSITY/employee_list.html', context)

def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    context = {
        'employee': employee,
        'university_name': 'Precious Cornerstone University'
    }
    return render(request, 'UNIVERSITY/employee_detail.html', context)

def employee_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')
    else:
        form = EmployeeForm()

    context = {
        'form': form,
        'university_name': 'Precious Cornerstone University'
    }
    return render(request, 'UNIVERSITY/employee_form.html', context)

def employee_update(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_detail', employee_id=employee.id)
    else:
        form = EmployeeForm(instance=employee)

    context = {
        'form': form,
        'employee': employee,
        'university_name': 'Precious Cornerstone University'
    }
    return render(request, 'UNIVERSITY/employee_form.html', context)

def employee_delete(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.method == 'POST':
        employee.delete()
        return redirect('employee_list')
    context = {
        'employee': employee,
        'university_name': 'Precious Cornerstone University'
    }
    return render(request, 'UNIVERSITY/employee_confirm_delete.html', context)


# --- Leave Management Views ---

def leave_list(request):
    leaves = Leave.objects.all().select_related('employee').order_by('-request_date')
    context = {
        'leaves': leaves,
        'university_name': 'Precious Cornerstone University'
    }
    return render(request, 'UNIVERSITY/leave_list.html', context)

def leave_detail(request, leave_id):
    leave = get_object_or_404(Leave, pk=leave_id)
    context = {
        'leave': leave,
        'university_name': 'Precious Cornerstone University'
    }
    return render(request, 'UNIVERSITY/leave_detail.html', context)

def leave_create(request):
    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('leave_list')
    else:
        form = LeaveForm()

    context = {
        'form': form,
        'university_name': 'Precious Cornerstone University'
    }
    return render(request, 'UNIVERSITY/leave_form.html', context)

def leave_update(request, leave_id):
    leave = get_object_or_404(Leave, pk=leave_id)
    if request.method == 'POST':
        form = LeaveForm(request.POST, instance=leave)
        if form.is_valid():
            form.save()
            return redirect('leave_detail', leave_id=leave.id)
    else:
        form = LeaveForm(instance=leave)

    context = {
        'form': form,
        'leave': leave,
        'university_name': 'Precious Cornerstone University'
    }
    return render(request, 'UNIVERSITY/leave_form.html', context)

def leave_delete(request, leave_id):
    leave = get_object_or_404(Leave, pk=leave_id)
    if request.method == 'POST':
        leave.delete()
        return redirect('leave_list')
    context = {
        'leave': leave,
        'university_name': 'Precious Cornerstone University'
    }
    return render(request, 'UNIVERSITY/leave_confirm_delete.html', context)


# --- NEW: Payroll Views ---

def payroll_list(request):
    """
    Displays a list of all payroll records.
    """
    payrolls = Payroll.objects.all().select_related('employee')
    context = {
        'payrolls': payrolls,
        'university_name': 'Precious Cornerstone University'
    }
    return render(request, 'UNIVERSITY/payroll_list.html', context)

def payroll_detail(request, pk):
    """
    Displays the details of a single payroll record.
    """
    payroll = get_object_or_404(Payroll, pk=pk)
    context = {
        'payroll': payroll,
        'university_name': 'Precious Cornerstone University'
    }
    return render(request, 'UNIVERSITY/payroll_detail.html', context)

def payroll_create(request):
    """
    Handles the creation of new payroll records using PayrollForm.
    """
    if request.method == 'POST':
        form = PayrollForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('payroll_list')
    else:
        form = PayrollForm()

    context = {
        'form': form,
        'university_name': 'Precious Cornerstone University',
        'is_edit': False,
        'title': 'Process New Payroll'
    }
    return render(request, 'UNIVERSITY/payroll_form.html', context)

# --- NEW: Student Views (Class-Based) ---
@method_decorator(login_required, name='dispatch')
class StudentListView(ListView):
    model = Student
    template_name = 'UNIVERSITY/student_list.html'
    context_object_name = 'students'
    ordering = ['last_name', 'first_name']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(student_id__icontains=query) | # Assuming student_id is a field in your Student model
                Q(email__icontains=query)
                # Add other fields you want to search by, e.g.,
                # Q(department__name__icontains=query) if Student has a foreign key to Department
            ).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['university_name'] = 'Precious Cornerstone University'
        context['query'] = self.request.GET.get('q', '') # Pass the query back to the template
        return context


@method_decorator(login_required, name='dispatch')
class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'UNIVERSITY/student_form.html'
    success_url = reverse_lazy('student_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['university_name'] = 'Precious Cornerstone University' # Added university_name
        return context

@method_decorator(login_required, name='dispatch')
class StudentDetailView(DetailView):
    model = Student
    template_name = 'UNIVERSITY/student_detail.html'
    context_object_name = 'student'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['university_name'] = 'Precious Cornerstone University' # Added university_name
        return context

@method_decorator(login_required, name='dispatch')
class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'UNIVERSITY/student_form.html'
    context_object_name = 'student'
    def get_success_url(self):
        return reverse_lazy('student_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['university_name'] = 'Precious Cornerstone University' # Added university_name
        return context

@method_decorator(login_required, name='dispatch')
class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'UNIVERSITY/student_confirm_delete.html'
    success_url = reverse_lazy('student_list')
    context_object_name = 'student'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['university_name'] = 'Precious Cornerstone University' # Added university_name
        return context
