from django.urls import path, include
from . import views
# UPDATED: Import all necessary Student and Course views
from .views import (
    StudentListView, StudentCreateView, StudentDetailView, StudentUpdateView, StudentDeleteView,
    CourseListView, CourseDetailView # Add these imports for class-based course views
)

urlpatterns = [
    # Existing URL patterns for Home, Registration
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),

    # UPDATED: Course URL patterns (now using class-based views)
    path('courses/', CourseListView.as_view(), name='course_list'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course_detail'), # Use <int:pk> for DetailView

    # Employee URL patterns (remain function-based as per your code)
    path('employees/', views.employee_list, name='employee_list'),
    path('employees/add/', views.employee_create, name='employee_create'),
    path('employees/<int:employee_id>/', views.employee_detail, name='employee_detail'),
    path('employees/<int:employee_id>/edit/', views.employee_update, name='employee_update'),
    path('employees/<int:employee_id>/delete/', views.employee_delete, name='employee_delete'),

    # Leave URL patterns (remain function-based as per your code)
    path('leaves/', views.leave_list, name='leave_list'),
    path('leaves/add/', views.leave_create, name='leave_create'),
    path('leaves/<int:leave_id>/', views.leave_detail, name='leave_detail'),
    path('leaves/<int:leave_id>/edit/', views.leave_update, name='leave_update'),
    path('leaves/<int:leave_id>/delete/', views.leave_delete, name='leave_delete'),

    # Payroll URL patterns (remain function-based as per your code)
    path('payroll/', views.payroll_list, name='payroll_list'),
    path('payroll/<int:pk>/', views.payroll_detail, name='payroll_detail'),
    path('payroll/add/', views.payroll_create, name='payroll_create'),

    # Student URL patterns (already class-based)
    path('students/', StudentListView.as_view(), name='student_list'),
    path('students/add/', StudentCreateView.as_view(), name='student_create'),
    path('students/<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
    path('students/<int:pk>/edit/', StudentUpdateView.as_view(), name='student_update'),
    path('students/<int:pk>/delete/', StudentDeleteView.as_view(), name='student_delete'),
]
