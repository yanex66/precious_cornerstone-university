# precious_cornerstone/PCU/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views # NEW: Import auth views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('university/', include('UNIVERSITY.urls')),
    path('', RedirectView.as_view(url='university/', permanent=True)),

    # Explicitly define password reset URLs and their templates
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html', # This line specifies the email template
        subject_template_name='registration/password_reset_subject.txt' # Optional: for email subject
    ), name='password_reset'),

    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),

    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),

    # You might want to keep other auth URLs if you need them, e.g., for login/logout:
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'), # Redirects to login after logout
]