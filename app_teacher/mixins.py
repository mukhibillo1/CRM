from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin): 
    allowed_roles = []

    def test_func(self):
        return self.request.user.role in self.allowed_roles  

    # def test_func(self):
    #     return True  # Временно разрешает всем пользователям доступ

    def handle_no_permission(self):
        user = self.request.user
        if not user.is_authenticated:
            return super().handle_no_permission()
        
        if user.role == 'manager':
            return redirect(reverse_lazy("manager:home"))
        elif user.role == 'teacher':
            return redirect(reverse_lazy("teacher:home"))
        elif user.role == 'reception':
            return redirect(reverse_lazy("reception:home"))
        return redirect(reverse_lazy("sign-in")) 