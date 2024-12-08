from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from functools import wraps
from django.shortcuts import redirect


class BarberRequiredMixin(UserPassesTestMixin):
    """Verify user is authenticated and has barber permissions"""
    def test_func(self):
        return self.request.user.has_perm('profiles.access_to_barber_actions')


class CustomerRequiredMixin(UserPassesTestMixin):
    """Verify user is authenticated and has customer permissions"""
    def test_func(self):
        return self.request.user.has_perm('profiles.access_to_customer_actions')
    


# def barber_required(f):
#     @wraps(f)
#     def g(request, *args, **kwargs):
#         if request.user.has_perm('profiles.access_to_barber_actions'):
#             return f(request, *args, **kwargs)
#         else:
#             return redirect('account_login')
#     return g


def barber_required(view_func):
    """
    Decorator to verify user is authenticated and has barber permissions.
    """
    def check_permissions(user):
        if not user.is_authenticated:
            return False
        if not user.has_perm('profiles.access_to_barber_actions'):
            return False
        return True

    # Applying user_passes_test decorator with the check_permissions function
    decorated_view_func = user_passes_test(check_permissions)(view_func)
    return decorated_view_func