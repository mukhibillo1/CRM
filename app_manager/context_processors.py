from app_common.models import Group

def groups_for_attendance(request):
    if request.user.is_authenticated and request.user.role in ['teacher', 'manager', 'receptionist']:
        return {'groups': Group.objects.all()}
    return {}
