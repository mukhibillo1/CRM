from django.contrib import admin
from .models import User, Course, Group, Lesson, Attendance, Lead, Payment,Teacher
from django.contrib.auth.admin import UserAdmin


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active')
    list_filter = ('role', 'is_active')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'role')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

    search_fields = ('username', 'email')
    ordering = ('username',)
    filter_horizontal = ('user_permissions',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'monthly_price')
    search_fields = ('title',)



@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'teacher', 'start_date', 'end_date')
    list_filter = ('course', 'start_date', 'end_date')
    search_fields = ('title', 'course__title', 'teacher__username')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'group', 'topic', 'date')
    list_filter = ('group', 'date')
    search_fields = ('topic', 'group__title')
    ordering = ('-date',)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'is_present', 'lesson')
    list_filter = ('lesson', 'is_present')
    search_fields = ('student__username',)


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'email', 'course', 'status', 'created_at')
    list_filter = ('status','created_at')
    search_fields = ('full_name', 'phone', 'email', 'course')
    ordering = ('-created_at',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'date')
    search_fields = ('student__username',)
    list_filter = ('date',)
    ordering = ['-date']






@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "last_name", "birth_date", "phone_or_email", "address")
    search_fields = ("name", "last_name", "phone_or_email")
    list_filter = ("birth_date",)
