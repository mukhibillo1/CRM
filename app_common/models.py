from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    groups = None
    ROLE_CHOICES = [
        ('manager', 'Manager'),
        ('teacher', 'Teacher'),
        ('receptionist', 'Receptionist'),
        ('accountant', 'Accountant'),
        ('student', 'Student'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)  # верни это
    monthly_price = models.DecimalField(max_digits=10, decimal_places=2, default=600000)

    def __str__(self):
        return self.title


class Group(models.Model):
    title = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': 'teacher'})
    students = models.ManyToManyField(User, through='StudentGroupInfo', related_name='groups')
    start_date = models.DateField()
    end_date = models.DateField()

    SCHEDULE_MODES = [
        ('workdays', 'Workdays (Mon–Sat)'),
        ('odd_days', 'Odd days (Mon, Wed, Fri)'),
        ('even_days', 'Even days (Tue, Thu, Sat)'),
    ]
    schedule_mode = models.CharField(max_length=20, choices=SCHEDULE_MODES, default='workdays')
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            from app_manager.views import create_lessons_for_group
            create_lessons_for_group(self, self.start_date, self.end_date)

    def __str__(self):
        return self.title


class StudentGroupInfo(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    last_payment = models.DateField(null=True, blank=True)

    STATUS_CHOICES = [
        ('ACTIVE', 'ACTIVE'),
        ('TRIAL', 'TRIAL'),
        ('FROZEN', 'FROZEN'),
        ('DEBTOR', 'DEBTOR'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')

    class Meta:
        unique_together = ('student', 'group')

    def __str__(self):
        return f"{self.student.username} — {self.group.title}"


class Lesson(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=100) 
    topic = models.CharField(max_length=100)  
    date = models.DateField()
 
    def __str__(self):
        return f"{self.group.title} - {self.title} - {self.topic} ({self.date})"


class Attendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_present = models.BooleanField()

    class Meta:
        unique_together = ('student', 'lesson')

    def __str__(self):
        return f"{self.student.username} - {self.lesson.date} - {'✔' if self.is_present else '✘'}"


class Payment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments', limit_choices_to={'role': 'student'})
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.student.username} — {self.amount} — {self.group.title}"


class Lead(models.Model):
    STATUS_CHOICES = [
        ('rejected', 'Rejected'),
        ('approved', 'Approved'),
        ('progress', 'In Progress'),
    ]

    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    budget = models.CharField(max_length=100, blank=True)
    technologies = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='progress')
    created_at = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.full_name
