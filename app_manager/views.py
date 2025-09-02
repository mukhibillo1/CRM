from django.views.generic import TemplateView
from app_common.mixins import RoleRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView
from helpers.views import CreateView, UpdateView, DeleteView
from app_common.models import Course, Group, Lesson, Attendance, Lead, Payment,User,Teacher
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from app_common.models import StudentGroupInfo
from app_common import forms
from django.db.models import Q
from django.http import JsonResponse
import json
from django.utils import timezone
from app_teacher.views import create_lessons_for_group
import calendar
from datetime import date, timedelta
from django.db.models import Count
class ManagerHomeView(RoleRequiredMixin, TemplateView):
    template_name = "manager/index.html"
    allowed_roles = ['manager']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'courses': Course.objects.all(),
            'groups': Group.objects.all(),
            'lessons': Lesson.objects.all(),
            'attendances': Attendance.objects.all(),
            'leads': Lead.objects.all(),
            'payments': Payment.objects.all(),
            'students': User.objects.filter(role='student'),
            'teachers': User.objects.filter(role='teacher'),
            'menu_parent': 'dashboard',
            'user':User.objects.all(),
        })
        return context




# Course
class CourseListView(RoleRequiredMixin, ListView):
    model = Course
    template_name = 'manager/courses/list.html'
    context_object_name = 'objects'
    allowed_roles = ['manager']
    paginate_by = 5

    def get_queryset(self):
        object_list = super().get_queryset()
        search = self.request.GET.get("search", None)
        if search:
            object_list = object_list.filter(Q(title__icontains=search))
        return object_list

class CourseCreateView(RoleRequiredMixin, CreateView):
    model = Course
    template_name = 'manager/courses/create.html'
    form_class = forms.CourseForm
    success_url = ('manager:course-list')
    allowed_roles = ['manager']
    success_create_url = "manager:course-create"
class CourseUpdateView(RoleRequiredMixin, UpdateView):
    model = Course
    template_name = 'manager/courses/update.html'
    form_class = forms.CourseForm
    success_url = ('manager:course-list')
    allowed_roles = ['manager']

class CourseDeleteView(RoleRequiredMixin, DeleteView):
    model = Course
    success_url = ('manager:course-list')
    allowed_roles = ['manager']


# Group
class GroupListView(RoleRequiredMixin, ListView):
    model = Group
    template_name = 'manager/groups/list.html'
    context_object_name = 'objects'
    allowed_roles = ['manager']
    paginate_by = 5

    def get_queryset(self):
        object_list = super().get_queryset()
        search = self.request.GET.get("search", None)
        if search:
            object_list = object_list.filter(Q(title__icontains=search))
        return object_list

class GroupCreateView(RoleRequiredMixin, CreateView):
    model = Group
    form_class = forms.GroupForm
    template_name = 'manager/groups/create.html'
    success_url = ('manager:group-list')
    allowed_roles = ['manager']
    success_create_url = "manager:group-create"

    def form_valid(self, form):
        response = super().form_valid(form)
        group = self.object
        create_lessons_for_group(group, group.start_date, group.end_date)
        return response


class GroupUpdateView(RoleRequiredMixin, UpdateView):
    model = Group
    template_name = 'manager/groups/update.html'
    form_class = forms.GroupForm
    success_url = ('manager:group-list')
    allowed_roles = ['manager']

class GroupDeleteView(RoleRequiredMixin, DeleteView):
    model = Group
    success_url = ('manager:group-list')
    allowed_roles = ['manager']


# Lesson
class LessonListView(RoleRequiredMixin, ListView):
    model = Lesson
    template_name = 'manager/lessons/list.html'
    context_object_name = 'objects'
    allowed_roles = ['manager']
    paginate_by = 5

    def get_queryset(self):
        object_list = Lesson.objects.all()
        search = self.request.GET.get("search")
        if search:
            object_list = object_list.filter(title__icontains=search)
        return object_list



class LessonCreateView(RoleRequiredMixin, CreateView):
    model = Lesson
    template_name = 'manager/lessons/create.html'
    form_class = forms.LessonForm
    success_url = ('manager:lesson-list')
    allowed_roles = ['manager']
    success_create_url = "manager:lesson-create"
class LessonUpdateView(RoleRequiredMixin, UpdateView):
    model = Lesson
    template_name = 'manager/lessons/update.html'
    form_class = forms.LessonForm
    success_url = ('manager:lesson-list')
    allowed_roles = ['manager']

class LessonDeleteView(RoleRequiredMixin, DeleteView):
    model = Lesson
    success_url = ('manager:lesson-list')
    allowed_roles = ['manager']



# Lead
class LeadListView(RoleRequiredMixin, ListView):
    model = Lead
    template_name = 'manager/leads/list.html'
    context_object_name = 'objects'
    allowed_roles = ['manager']
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        period = self.request.GET.get('period')

        if status:
            queryset = queryset.filter(status=status)

        if period == 'month':
            queryset = queryset.filter(created_at__month=timezone.now().month)
        elif period == 'week':
            today = timezone.now().date()
            start_week = today - timedelta(days=today.weekday())
            end_week = start_week + timedelta(days=6)
            queryset = queryset.filter(created_at__date__range=(start_week, end_week))
        elif period == 'day':
            queryset = queryset.filter(created_at__date=timezone.now().date())

        return queryset

class LeadCreateView(RoleRequiredMixin, CreateView):
    model = Lead
    template_name = 'manager/leads/create.html'
    form_class = forms.LeadForm
    success_url = ('manager:lead-list')
    allowed_roles = ['manager']
    success_create_url = "manager:lead-create"
class LeadUpdateView(RoleRequiredMixin, UpdateView):
    model = Lead
    template_name = 'manager/leads/update.html'
    form_class = forms.LeadForm
    success_url = ('manager:lead-list')
    allowed_roles = ['manager']

class LeadDeleteView(RoleRequiredMixin, DeleteView):
    model = Lead
    success_url = ('manager:lead-list')
    allowed_roles = ['manager']



class LeadStatusStatsView(View):
    def get(self, request, *args, **kwargs):
        STATUS_LABELS = {
            'rejected': 'Rejected',
            'approved': 'Approved',
            'progress': 'In Progress',  
        }

        raw_data = Lead.objects.values('status').annotate(count=Count('id'))
        formatted_data = [
            {
                'status': STATUS_LABELS.get(item['status'], 'Unknown'),
                'count': item['count']
            }
            for item in raw_data
        ]

        return JsonResponse(formatted_data, safe=False)


class AttendanceJournalView(RoleRequiredMixin, TemplateView):
    template_name = 'manager/attendance/gradebook.html'
    allowed_roles = ['manager']

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
        # 🔧 Вызываем payment() здесь
        for student in students:
            student.payments.all()
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

class GroupAttendanceStatsView(RoleRequiredMixin, View):
    allowed_roles = ['manager']
    
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


class PaymentListView(RoleRequiredMixin, ListView):
    model = Payment
    template_name = 'manager/payments/list.html'
    context_object_name = 'objects'
    allowed_roles = ['manager']

class PaymentCreateView(RoleRequiredMixin, CreateView):
    model = Payment
    form_class = forms.PaymentForm
    template_name = 'manager/payments/create.html'
    success_url = ('manager:payment-list')
    allowed_roles = ['manager']
    success_create_url = "manager:payment-create"

    def form_valid(self, form):
        response = super().form_valid(form)
        payment = form.instance
        # 💡 можно обновить баланс вручную, если у тебя ещё осталась такая логика
        group_info = StudentGroupInfo.objects.filter(student=payment.student, group=payment.group).first()
        if group_info:
            group_info.balance += payment.amount
            group_info.last_payment = payment.date
            group_info.save()
        return response



class PaymentUpdateView(RoleRequiredMixin, UpdateView):
    model = Payment
    form_class = forms.PaymentForm
    template_name = 'manager/payments/update.html'
    success_url = ('manager:payment-list')
    allowed_roles = ['manager']

    def form_valid(self, form):
        old_payment = self.get_object()
        old_amount = old_payment.amount
        response = super().form_valid(form)
        payment = form.instance
        group_info = StudentGroupInfo.objects.filter(student=payment.student, group=payment.group).first()
        if group_info:
            group_info.balance -= old_amount
            group_info.balance += payment.amount
            group_info.last_payment = payment.date
            group_info.save()
        return response



class PaymentDeleteView(RoleRequiredMixin, DeleteView):
    model = Payment
    success_url = ('manager:payment-list')
    allowed_roles = ['manager']


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





def custom_404(request, exception):
    return render(request, 'pages/404.html', status=404)








class UserListView(ListView):
    model = User
    template_name = "manager/user/list.html"
    context_object_name = "objects"  # template'da objects ishlatiladi

    paginate_by = 10


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request  # formga request yuboramiz
        return kwargs

class UserCreateView(CreateView):
    model = User
    form_class = forms.UserForm
    template_name = "manager/user/create.html"
    context_object_name = "object"
    success_url = "manager:user-list"
    success_create_url = "manager:user-create"


class UserUpdateView(UpdateView):
    model = User
    form_class = forms.UserForm
    template_name = "manager/user/update.html"
    context_object_name = "object"
    success_url = "manager:user-list"
    success_update_url = "manager:user-update"


class UserDeleteView(DeleteView):
    model = User
    success_url = "manager:user-list"




class TeacherListView( ListView):

    model = Teacher
    template_name = "manager/teachers/list.html"

    context_object_name = "objects"
    paginate_by = 10

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request  # formga request yuboramiz
        return kwargs


class TeacherCreateView(CreateView):

    model = Teacher
    form_class = forms.TeacherForm
    template_name = "manager/teachers/create.html"
    context_object_name = "object"
    success_url = "manager:teacher-list"
    success_create_url = "manager:teacher-create"


class TeacherUpdateView(UpdateView):

    model = Teacher
    form_class = forms.TeacherForm
    template_name = "manager/teachers/update.html"
    context_object_name = "object"
    success_url = "manager:teacher-list"
    success_update_url = "manager:teacher-update"


class TeacherDeleteView(DeleteView):

    model = Teacher
    success_url = "manager:teacher-list"




