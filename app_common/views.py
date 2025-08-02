from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from helpers.views import CreateView, UpdateView, DeleteView
from .models import Course, Group, Lesson, Attendance, Lead, Payment,User
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from . import mixins
from django.contrib.auth.decorators import login_required, user_passes_test
from . import forms
from django.db.models import Q
from django.utils.timezone import now
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.generic.edit import CreateView
from .models import Group
from .forms import GroupForm
from app_teacher.views import create_lessons_for_group
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test

class HomeView(View):
    def get(self, request): 
        context = {
        }
        return render(request, "index.html", context)
    
# Course
class CourseListView(mixins.RoleRequiredMixin, ListView):
    model = Course
    template_name = 'courses/list.html'
    context_object_name = 'objects'
    allowed_roles = ['manager', 'receptionist', 'teacher']
    paginate_by = 5

    def get_queryset(self):
        object_list = super().get_queryset()
        search = self.request.GET.get("search", None)
        if search:
            object_list = object_list.filter(Q(title__icontains=search))
        return object_list

class CourseCreateView(mixins.RoleRequiredMixin, CreateView):
    model = Course
    template_name = 'courses/create.html'
    form_class = forms.CourseForm
    success_url = ('common:course-list')
    allowed_roles = ['manager']

class CourseUpdateView(mixins.RoleRequiredMixin, UpdateView):
    model = Course
    template_name = 'courses/update.html'
    form_class = forms.CourseForm
    success_url = ('common:course-list')
    allowed_roles = ['manager']

class CourseDeleteView(mixins.RoleRequiredMixin, DeleteView):
    model = Course
    success_url = ('common:course-list')
    allowed_roles = ['manager']


# Group
class GroupListView(mixins.RoleRequiredMixin, ListView):
    model = Group
    template_name = 'groups/list.html'
    context_object_name = 'objects'
    allowed_roles = ['manager', 'teacher', 'receptionist']
    paginate_by = 5

    def get_queryset(self):
        object_list = super().get_queryset()
        search = self.request.GET.get("search", None)
        if search:
            object_list = object_list.filter(Q(title__icontains=search))
        return object_list

class GroupCreateView(mixins.RoleRequiredMixin, CreateView):
    model = Group
    form_class = forms.GroupForm
    template_name = 'groups/create.html'
    success_url = ('common:group-list')
    allowed_roles = ['manager', 'receptionist']

    def form_valid(self, form):
        response = super().form_valid(form)
        group = self.object
        create_lessons_for_group(group, group.start_date, group.end_date)
        return response


class GroupUpdateView(mixins.RoleRequiredMixin, UpdateView):
    model = Group
    template_name = 'groups/update.html'
    form_class = forms.GroupForm
    success_url = ('common:group-list')
    allowed_roles = ['manager', 'receptionist']

class GroupDeleteView(mixins.RoleRequiredMixin, DeleteView):
    model = Group
    success_url = ('common:group-list')
    allowed_roles = ['manager',]


# Lesson
class LessonListView(mixins.RoleRequiredMixin, ListView):
    model = Lesson
    template_name = 'lessons/list.html'
    context_object_name = 'objects'
    allowed_roles = ['manager', 'teacher', 'receptionist']
    paginate_by = 5

    def get_queryset(self):
        object_list = Lesson.objects.all()
        search = self.request.GET.get("search")
        if search:
            object_list = object_list.filter(title__icontains=search)
        return object_list



class LessonCreateView(mixins.RoleRequiredMixin, CreateView):
    model = Lesson
    template_name = 'lessons/create.html'
    form_class = forms.LessonForm
    success_url = ('common:lesson-list')
    allowed_roles = ['teacher', 'manager']

class LessonUpdateView(mixins.RoleRequiredMixin, UpdateView):
    model = Lesson
    template_name = 'lessons/update.html'
    form_class = forms.LessonForm
    success_url = ('common:lesson-list')
    allowed_roles = ['teacher', 'manager']

class LessonDeleteView(mixins.RoleRequiredMixin, DeleteView):
    model = Lesson
    success_url = ('common:lesson-list')
    allowed_roles = ['manager', 'teacher']


# Attendance
class AttendanceListView(mixins.RoleRequiredMixin, ListView):
    model = Attendance
    template_name = 'attendance/list.html'
    context_object_name = 'objects'
    allowed_roles = ['manager', 'teacher']
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(Q(title__icontains=search))  
        return queryset

class AttendanceCreateView(mixins.RoleRequiredMixin, CreateView):
    model = Attendance

    template_name = 'attendance/create.html'
    form_class = forms.AttendanceForm
    success_url = ('common:attendance-list')
    allowed_roles = ['manager','teacher']

class AttendanceUpdateView(mixins.RoleRequiredMixin, UpdateView):
    model = Attendance
    template_name = 'attendance/update.html'
    form_class = forms.AttendanceForm
    success_url = ('common:attendance-list')
    allowed_roles = ['teacher','manager']

class AttendanceDeleteView(mixins.RoleRequiredMixin, DeleteView):
    model = Attendance
    success_url = ('common:attendance-list')
    allowed_roles = ['manager']



# Lead
class LeadListView(mixins.RoleRequiredMixin, ListView):
    model = Lead
    template_name = 'leads/list.html'
    context_object_name = 'objects'
    allowed_roles = ['manager', 'receptionist']
    paginate_by = 5
    def get_queryset(self):
        object_list = self.queryset
        search = self.request.GET.get("search", None)
        if search:
            object_list = object_list.filter(Q(title__icontains=search))

        return object_list

class LeadCreateView(mixins.RoleRequiredMixin, CreateView):
    model = Lead

    template_name = 'leads/create.html'
    form_class = forms.LeadForm
    success_url = ('common:lead-list')
    allowed_roles = ['manager', 'receptionist']

class LeadUpdateView(mixins.RoleRequiredMixin, UpdateView):
    model = Lead
    template_name = 'leads/update.html'
    form_class = forms.LeadForm
    success_url = ('common:lead-list')
    allowed_roles = ['manager', 'receptionist']

class LeadDeleteView(mixins.RoleRequiredMixin, DeleteView):
    model = Lead
    success_url = ('common:lead-list')
    allowed_roles = ['manager', 'receptionist']


def root_redirect_view(request):
    if request.user.is_authenticated:
        role = request.user.role
        if role == 'manager':
            return redirect(reverse_lazy("manager:home"))
        elif role == 'teacher':
            return redirect(reverse_lazy("teacher:home"))
        elif role == 'reception':
            return redirect(reverse_lazy("reception:home"))
    return redirect(reverse_lazy("sign-in"))


# Authenticate
class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return self.redirect_by_role(request.user)
        return render(request, "pages/sign-in.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return self.redirect_by_role(user)
        return render(request, "pages/sign-in.html", {"error": True})

    def redirect_by_role(self, user):
        if user.role == 'manager':
            return HttpResponseRedirect(reverse_lazy("manager:home"))
        elif user.role == 'teacher':
            return HttpResponseRedirect(reverse_lazy("teacher:home"))
        elif user.role == 'reception':
            return HttpResponseRedirect(reverse_lazy("reception:home"))
        return HttpResponseRedirect("/")

class SignoutView(View, LoginRequiredMixin):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse_lazy("sign-in"))


def custom_404(request, exception):
    return render(request, 'pages/404.html', status=404)



def attendance_journal(request):
    students = User.objects.filter(role='student')
    lessons = Lesson.objects.select_related('group').order_by('date')
    attendances = Attendance.objects.filter(student__in=students)

    attendance_map = {}
    for att in attendances:
        attendance_map.setdefault(att.student_id, {})[att.lesson_id] = att

    return render(request, 'app_manager/attendance/gradebook.html', {
        'students': students,
        'lessons': lessons,
        'attendance': attendance_map,
    })



@csrf_exempt
def update_attendance(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        student_id = data.get('student_id')
        lesson_id = data.get('lesson_id')
        is_present = data.get('is_present')

        student = User.objects.get(id=student_id)
        lesson = Lesson.objects.get(id=lesson_id)

        attendance, created = Attendance.objects.get_or_create(student=student, lesson=lesson)
        attendance.is_present = is_present
        attendance.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=400)



def is_manager(user):
    return user.is_authenticated and user.role == 'manager'

@login_required
@user_passes_test(is_manager)
def payment_create(request):
    if request.method == 'POST':
        form = forms.PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            if payment.status == 'paid':
                payment.paid_at = now()
            payment.save()
            return redirect('common:payment-list')
    else:
        form = forms.PaymentForm()
    return render(request, 'payments/create.html', {'form': form})












@login_required
@user_passes_test(is_manager)
def payment_list(request):
    payments = Payment.objects.select_related('student', 'course').order_by('-created_at')
    return render(request, 'payments/list.html', {'payments': payments})


