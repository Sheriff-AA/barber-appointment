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
    

class OwnershipMixin:
    """
    A mixin to check if the request.user is the owner of the target object or related models.
    For TemplateView, the object must be explicitly defined or fetched in the mixin.
    """
    def get_target_object(self):
        """
        Override this method in the view to define how to get the target object.
        """
        raise NotImplementedError(
            "You must define `get_target_object` in your view or provide an object fetching method."
        )

    def dispatch(self, request, *args, **kwargs):
        # Fetch the object to check ownership
        kwargs['is_owner'] = is_owner = False
        obj = self.get_target_object()

        # Determine ownership
        is_owner = False

        if hasattr(obj, 'user') and obj.user == request.user:
            is_owner = True

        # Check related model ownership if needed
        related_models = getattr(obj, 'related_models', [])
        for related in related_models:
            if hasattr(related, 'user') and related.user == request.user:
                is_owner = True
                break

        # Add the `is_owner` flag to kwargs for use in the context
        kwargs['is_owner'] = is_owner

        return super().dispatch(request, *args, **kwargs)
    

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