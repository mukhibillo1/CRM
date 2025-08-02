from django.views.generic import TemplateView, ListView, View
from app_common import mixins
from app_common.models import Course, Group, Attendance, Lesson, User
from app_common import forms
from django.db.models import Q
from django.http import JsonResponse
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from datetime import date
from django.utils import timezone
from helpers.views import CreateView, UpdateView, DeleteView
import calendar
from datetime import date, timedelta

class TeacherHomeView(mixins.RoleRequiredMixin, TemplateView):
    template_name = "teacher/index.html"
    allowed_roles = ['teacher']
class CourseListView(mixins.RoleRequiredMixin, ListView):
    model = Course
    template_name = 'teacher/courses/list.html'
    context_object_name = 'objects'
    allowed_roles = ['teacher']
    paginate_by = 5

    def get_queryset(self):
        object_list = super().get_queryset()
        search = self.request.GET.get("search", None)
        if search:
            object_list = object_list.filter(Q(title__icontains=search))
        return object_list
class GroupListView(mixins.RoleRequiredMixin, ListView):
    model = Group
    template_name = 'teacher/groups/list.html'
    context_object_name = 'objects'
    allowed_roles = ['teacher']
    paginate_by = 5

    def get_queryset(self):
        object_list = super().get_queryset()
        search = self.request.GET.get("search", None)
        if search:
            object_list = object_list.filter(Q(title__icontains=search))
        return object_list
class LessonListView(mixins.RoleRequiredMixin, ListView):
    model = Lesson
    template_name = 'teacher/lessons/list.html'
    context_object_name = 'objects'
    allowed_roles = ['teacher']
    paginate_by = 5

    def get_queryset(self):
        object_list = Lesson.objects.all()
        search = self.request.GET.get("search")
        if search:
            object_list = object_list.filter(title__icontains=search)
        return object_list
    

class LessonCreateView(mixins.RoleRequiredMixin, CreateView):
    model = Lesson
    template_name = 'teacher/lessons/create.html'
    form_class = forms.LessonForm
    success_url = ('teacher:lesson-list')
    allowed_roles = ['teacher']
    success_create_url = "teacher:lesson-create"
class LessonUpdateView(mixins.RoleRequiredMixin, UpdateView):
    model = Lesson
    template_name = 'teacher/lessons/update.html'
    form_class = forms.LessonForm
    success_url = ('teacher:lesson-list')
    allowed_roles = ['teacher']

class LessonDeleteView(mixins.RoleRequiredMixin, DeleteView):
    model = Lesson
    success_url = ('teacher:lesson-list')
    allowed_roles = ['teacher']


class AttendanceJournalView(mixins.RoleRequiredMixin, TemplateView):
    template_name = 'teacher/attendance/gradebook.html'
    allowed_roles = ['teacher']

    def get_group(self):
        group_id = self.kwargs.get('group_id')
        return get_object_or_404(Group, id=group_id)

    def get_selected_month_year(self):
        today = timezone.now().date()
        year = int(self.request.GET.get('year', today.year))
        month = int(self.request.GET.get('month', today.month))
        return year, month, today

    def get_students(self, group, search):
        students = group.students.all()
        if search:
            students = students.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(username__icontains=search)
            )
        return students

    def get_lessons(self, group, year, month):
        return Lesson.objects.filter(
            group=group,
            date__year=year,
            date__month=month
        ).order_by('date')

    def get_attendance_map(self, students, lessons):
        attendances = Attendance.objects.filter(student__in=students, lesson__in=lessons)
        attendance_map = {}
        for att in attendances:
            attendance_map.setdefault(att.student_id, {})[att.lesson_id] = att
        return attendance_map

    def get_years(self, group):
        all_years = Lesson.objects.filter(group=group).dates('date', 'year')
        return sorted(set(y.year for y in all_years), reverse=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        group = self.get_group()
        selected_year, selected_month, today = self.get_selected_month_year()
        search_query = self.request.GET.get("search", "")
        lessons = self.get_lessons(group, selected_year, selected_month)
        students = self.get_students(group, search_query)
        attendance_map = self.get_attendance_map(students, lessons)
        years = self.get_years(group)

        months = [
            (1, 'Yanvar'), (2, 'Fevral'), (3, 'Mart'), (4, 'Aprel'),
            (5, 'May'), (6, 'Iyun'), (7, 'Iyul'), (8, 'Avgust'),
            (9, 'Sentabr'), (10, 'Oktabr'), (11, 'Noyabr'), (12, 'Dekabr'),
        ]

        context.update({
            'groups': Group.objects.all(),
            'menu_parent': 'attendance',
            'menu_child': f'attendance-{group.id}',
            'group': group,
            'students': students,
            'lessons': lessons,
            'attendance': attendance_map,
            'years': years,
            'months': months,
            'selected_year': selected_year,
            'selected_month': selected_month,
            'today': today,
            'search': search_query,
        })
        return context


@method_decorator(csrf_exempt, name='dispatch')
class UpdateAttendanceView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            student_id = data.get('student_id')
            lesson_id = data.get('lesson_id')
            is_present = data.get('is_present')

            student = User.objects.get(id=student_id)
            lesson = Lesson.objects.get(id=lesson_id)

            attendance, created = Attendance.objects.get_or_create(
                student=student,
                lesson=lesson,
                defaults={'is_present': is_present}
            )

            if not created:
                attendance.is_present = is_present
                attendance.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    def get(self, request, *args, **kwargs):
        return JsonResponse({'success': False}, status=400)

class GroupAttendanceStatsView(mixins.RoleRequiredMixin, View):
    allowed_roles = ['teacher']

    def get(self, request, group_id):
        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return JsonResponse({'error': 'Group not found'}, status=404)

        year = int(request.GET.get('year', timezone.now().year))
        month = int(request.GET.get('month', timezone.now().month))

        lessons = Lesson.objects.filter(
            group=group,
            date__year=year,
            date__month=month
        ).order_by('date')

        students = group.students.all()
        lesson_days = lessons.values_list('date', flat=True).distinct().count()
        today = timezone.now().date()
        if lessons.filter(date=today).exists():
            target_date = today
        else:
            first_lesson = lessons.first()
            if not first_lesson:
                return JsonResponse({
                    'total_students': students.count(),
                    'total_lessons': 0,
                    'total_present': 0,
                    'total_absent': 0
                })
            target_date = first_lesson.date

        day_lessons = lessons.filter(date=target_date)

        total_present = Attendance.objects.filter(
            lesson__in=day_lessons,
            student__in=students,
            is_present=True
        ).count()

        total_absent = Attendance.objects.filter(
            lesson__in=day_lessons,
            student__in=students,
            is_present=False
        ).count()

        return JsonResponse({
            'total_students': students.count(),
            'total_lessons': lesson_days,  
            'total_present': total_present, 
            'total_absent': total_absent   
        })


def create_lessons_for_group(group, start_date=None, end_date=None):
    if not start_date:
        start_date = date.today().replace(day=1)
    if not end_date:
        last_day = calendar.monthrange(start_date.year, start_date.month)[1]
        end_date = date(start_date.year, start_date.month, last_day)

    days_map = {
        'workdays': [0,1,2,3,4,5],
        'odd_days': [0,2,4],
        'even_days': [1,3,5],
    }

    weekdays = days_map.get(group.schedule_mode, [])
    current_day = start_date

    while current_day <= end_date:
        if current_day.weekday() in weekdays:
            Lesson.objects.get_or_create(
                group=group,
                course=group.course,  
                date=current_day,
                defaults={"title": f"{calendar.day_name[current_day.weekday()]} lesson"}
            )
        current_day += timedelta(days=1)
