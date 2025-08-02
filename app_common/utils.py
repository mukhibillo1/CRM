from django.utils import timezone
from .models import Lesson, StudentGroupInfo

def update_payment_status(student, group):
    info = StudentGroupInfo.objects.get(student=student, group=group)
    today = timezone.now().date()
    lessons = Lesson.objects.filter(
        group=group,
        date__year=today.year,
        date__month=today.month
    )
    total_lessons = lessons.count()
    if total_lessons == 0:
        return

    price_per_lesson = group.course.monthly_price / total_lessons
    attended_lessons = lessons.filter(attendance__student=student, attendance__is_present=True).count()

    charged = attended_lessons * price_per_lesson
    info.balance -= charged

    if info.balance < 0:
        info.status = 'DEBTOR'
    elif info.status != 'FROZEN':
        info.status = 'ACTIVE'

    info.last_payment = today
    info.save()
