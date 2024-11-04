# decorators.py
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse

def role_required(*roles):

    def in_roles(user):
        # Check if the user is authenticated and has one of the specified roles
        return user.is_authenticated and user.role in roles

    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            # Determine login URL based on specified roles
            if 'client' in roles:
                login_url = reverse('account:client_login')
            else:
                login_url = reverse('account:employee_login')

            # Check if the user has the correct role, redirecting if not
            return user_passes_test(in_roles, login_url=login_url)(view_func)(request, *args, **kwargs)

        return wrapper

    return decorator
