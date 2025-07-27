# precious_cornerstone/UNIVERSITY/middleware.py

import re
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse # Used to construct URLs by name

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Define URL patterns that do NOT require login.
        # These are regular expressions.
        # We use re.compile for efficiency as the middleware initializes once.
        self.exempt_url_patterns = [
            re.compile(r'^%s$' % settings.LOGIN_URL.lstrip('/')), # Login page (e.g., ^accounts/login/$)
            re.compile(r'^%s$' % reverse('register').lstrip('/')), # Registration page (e.g., ^register/$)

            # Password reset flow URLs:
            re.compile(r'^%s$' % reverse('password_reset').lstrip('/')), # /accounts/password_reset/
            re.compile(r'^%s$' % reverse('password_reset_done').lstrip('/')), # /accounts/password_reset/done/
            # This matches /accounts/reset/uidb64/token/ - [^/]+ matches one or more non-slash characters
            re.compile(r'^%s[^/]+/[^/]+/$' % reverse('password_reset_confirm', args=['x','y']).replace('x/y', '').lstrip('/')),
            re.compile(r'^%s$' % reverse('password_reset_complete').lstrip('/')), # /accounts/reset/done/

            # Allow access to admin login (for staff/superusers)
            re.compile(r'^admin/login/$'),
            # If you have other universally public pages (like an 'about' page), add them here:
            # re.compile(r'^university/about/$'),
        ]

    def __call__(self, request):
        # 1. Allow requests for static files (CSS, JS, images)
        if request.path.startswith(settings.STATIC_URL):
            return self.get_response(request)

        # 2. Allow access to the Django Admin interface itself for authenticated staff
        # Django's admin app handles its own authentication and permissions internally.
        if request.path.startswith('/admin/'):
            return self.get_response(request)

        # 3. If the user is already authenticated, allow them to proceed
        if request.user.is_authenticated:
            return self.get_response(request)

        # 4. Check if the requested URL is in the exempt list (doesn't require login)
        path = request.path_info.lstrip('/') # Get the URL path without a leading slash
        for pattern in self.exempt_url_patterns:
            if pattern.match(path):
                return self.get_response(request)

        # 5. If not authenticated and not exempt, redirect to the login page.
        #    We add '?next=' parameter so the user is redirected back to their intended page after logging in.
        current_path = request.path
        # Avoid redirecting to login page if we are already on the login page (prevents infinite loop)
        if current_path != settings.LOGIN_URL:
            return redirect(f"{settings.LOGIN_URL}?next={current_path}")

        # If we reached here, it means the user is on the LOGIN_URL itself, so let the request pass
        return self.get_response(request)