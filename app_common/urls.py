from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
# from .views import register_user

app_name = 'common'
urlpatterns = [ 
    path('', views.root_redirect_view, name='redicret'), 

    # Courses
    path('courses/', views.CourseListView.as_view(), name='course-list'),
    path('courses/create/', views.CourseCreateView.as_view(), name='course-create'),
    path('courses/<int:pk>/update/', views.CourseUpdateView.as_view(), name='course-update'),
    path('courses/<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course-delete'),
    # Groups
    path('groups/', views.GroupListView.as_view(), name='group-list'),
    path('groups/create/', views.GroupCreateView.as_view(), name='group-create'),
    path('groups/<int:pk>/update/', views.GroupUpdateView.as_view(), name='group-update'),
    path('groups/<int:pk>/delete/', views.GroupDeleteView.as_view(), name='group-delete'),
    # Lessons
    path('lessons/', views.LessonListView.as_view(), name='lesson-list'),
    path('lessons/create/', views.LessonCreateView.as_view(), name='lesson-create'),
    path('lessons/<int:pk>/update/', views.LessonUpdateView.as_view(), name='lesson-update'),
    path('lessons/<int:pk>/delete/', views.LessonDeleteView.as_view(), name='lesson-delete'),
    # Attendance
    path('attendance/', views.AttendanceListView.as_view(), name='attendance-list'),
    path('attendance/create/', views.AttendanceCreateView.as_view(), name='attendance-create'),
    path('attendance/<int:pk>/update/', views.AttendanceUpdateView.as_view(), name='attendance-update'),
    path('attendance/<int:pk>/delete/', views.AttendanceDeleteView.as_view(), name='attendance-delete'),
    # Leads
    path('leads/', views.LeadListView.as_view(), name='lead-list'),
    path('leads/create/', views.LeadCreateView.as_view(), name='lead-create'),
    path('leads/<int:pk>/update/', views.LeadUpdateView.as_view(), name='lead-update'),
    path('leads/<int:pk>/delete/', views.LeadDeleteView.as_view(), name='lead-delete'),

    
    # reg teacher/st
    # path('register-user/', register_user, name='register-user'),


    #paymant
    path('attendance/update/', views.update_attendance, name='update_attendance'),
    path('attendance/gradebook/', views.attendance_journal, name='gradebook'),
    path('payments/', views.payment_list, name='payment-list'),
    path('payments/create/', views.payment_create, name='payment-create'),

]

