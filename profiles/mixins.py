from django.contrib.auth.mixins import UserPassesTestMixin


class BarberRequiredMixin(UserPassesTestMixin):
    """Verify user is authenticated and has barber permissions"""
    def test_func(self):
        return self.request.user.has_perm('profiles.barber_actions')


class CustomerRequiredMixin(UserPassesTestMixin):
    """Verify user is authenticated and has customer permissions"""
    def test_func(self):
        return self.request.user.has_perm('profiles.customer_actions')