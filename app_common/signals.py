from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Attendance, Group
from .utils import update_payment_status
from app_teacher.views import create_lessons_for_group

@receiver(post_save, sender=Attendance)
def update_balance_after_attendance(sender, instance, created, **kwargs):
    if created and instance.is_present:
        update_payment_status(instance.student, instance.lesson.group)

@receiver(post_save, sender=Group)
def create_lessons_on_group_create(sender, instance, created, **kwargs):
    if created:
        create_lessons_for_group(instance, instance.start_date, instance.end_date)
