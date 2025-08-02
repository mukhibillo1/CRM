from django.views.generic import TemplateView
from app_common.mixins import RoleRequiredMixin

class ReceptionHomeView(RoleRequiredMixin, TemplateView):
    template_name = "receptionist/index.html"
    allowed_roles = ['reception']
