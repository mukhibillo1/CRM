from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def get_item(dictionary, key):
    if dictionary is None:
        return None
    return dictionary.get(key)

MONTHS_EN = [
    "", "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

@register.filter
def get_month_name(month_number):
    try:
        return MONTHS_EN[int(month_number)]
    except (ValueError, IndexError):
        return ""


@register.simple_tag
def student_status_icon(student, group):
    try:
        info = student.studentgroupinfo_set.get(group=group)
        status = info.status
    except:
        return ""  # если инфы нет — не показываем иконку

    if status == 'FROZEN':
        return mark_safe('<i class="fas fa-snowflake text-primary" title="Frozen"></i>')
    elif status == 'DEBTOR':
        return mark_safe('<i class="fas fa-circle text-danger" title="Debtor"></i>')
    elif status == 'ACTIVE':
        return mark_safe('<i class="fas fa-circle text-success" title="Active"></i>')
    else:
        return ""