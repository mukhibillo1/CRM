from django.urls import path
from . import views

app_name = "teacher"

urlpatterns = [
    path('', views.TeacherHomeView.as_view(), name="home"),
    path('courses/', views.CourseListView.as_view(), name='course-list'),
    path('groups/', views.GroupListView.as_view(), name='group-list'),
    path('lessons/', views.LessonListView.as_view(), name='lesson-list'),
    path('lessons/create/', views.LessonCreateView.as_view(), name='lesson-create'),
    path('lessons/<int:pk>/update/', views.LessonUpdateView.as_view(), name='lesson-update'),
    path('lessons/<int:pk>/delete/', views.LessonDeleteView.as_view(), name='lesson-delete'),
    path('attendance/journal/<int:group_id>/', views.AttendanceJournalView.as_view(), name='attendance_journal'),
    path('attendance/update/', views.UpdateAttendanceView.as_view(), name='update_attendance'),
    path('attendance/stats/<int:group_id>/', views.GroupAttendanceStatsView.as_view(), name='group_attendance_stats'),



]
