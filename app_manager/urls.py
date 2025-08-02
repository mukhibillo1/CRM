from django.urls import path
from . import views

app_name = "manager"
 
urlpatterns = [
    path('', views.ManagerHomeView.as_view(), name="home"),
    path('attendance/journal/<int:group_id>/', views.AttendanceJournalView.as_view(), name='attendance_journal'),
    path('attendance/update/', views.UpdateAttendanceView.as_view(), name='update_attendance'),
    path('attendance/stats/<int:group_id>/', views.GroupAttendanceStatsView.as_view(), name='group_attendance_stats'),

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
    path('attendance/journal/<int:group_id>/', views.AttendanceJournalView.as_view(), name='attendance_journal'),
    path('attendance/update/', views.UpdateAttendanceView.as_view(), name='update_attendance'),
    path('attendance/stats/<int:group_id>/', views.GroupAttendanceStatsView.as_view(), name='group_attendance_stats'),
    # Leads
    path('leads/', views.LeadListView.as_view(), name='lead-list'),
    path('leads/create/', views.LeadCreateView.as_view(), name='lead-create'),
    path('leads/<int:pk>/update/', views.LeadUpdateView.as_view(), name='lead-update'),
    path('leads/<int:pk>/delete/', views.LeadDeleteView.as_view(), name='lead-delete'),
    path('leads/status-stats/', views.LeadStatusStatsView.as_view(), name='lead-status-stats'),
    path("leads/", views.LeadListView.as_view(), name="lead-list"),
    #payments
    path('payments/create/', views.PaymentCreateView.as_view(), name='payment-create'),
    path('payments/<int:pk>/update/', views.PaymentUpdateView.as_view(), name='payment-update'),
    path('payments/', views.PaymentListView.as_view(), name='payment-list'),
    path('payments/<int:pk>/delete/', views.LessonDeleteView.as_view(), name='payment-delete'),


]
