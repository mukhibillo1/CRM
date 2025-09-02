from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Course, Group, Lesson, Attendance, Lead, Payment,Teacher
from helpers import widgets as widget
from ckeditor.widgets import CKEditorWidget
from . import models
from helpers import widgets


# forms.py
class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'role': forms.Select(attrs={'class': 'form-control', 'id': 'kt_select2_1'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'role' in self.fields:
            # "Manager" ni olib tashlash
            self.fields['role'].choices = [
                (value, label) for value, label in self.fields['role'].choices
                if label != 'Manager'
            ]



class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'monthly_price']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Course Title'}),
            'description': CKEditorWidget(attrs={'class': 'form-control', 'placeholder': 'Course Description'}),
            'monthly_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Course Price'}),
        }





class GroupForm(forms.ModelForm):
    students = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role='student'),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
            'id': 'kt_select2_11',
            'data-placeholder': 'Add students'
        })
    )

    class Meta:
        model = Group
        fields = ['title', 'course', 'teacher', 'students', 'start_date', 'end_date', 'schedule_mode']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Group Title'}),
            'course': forms.Select(attrs={'class': 'form-control', 'id': 'kt_select2_1'}),
            'teacher': forms.Select(attrs={'class': 'form-control', 'id': 'kt_select2_2'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Start Date', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'End Date', 'type': 'date'}),
            'schedule_mode': forms.Select(attrs={'class': 'form-control', 'id': 'kt_select2'}),
        }



class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'topic', 'date', 'group']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lesson Title'}),
            'topic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lesson Topic'}),
            'date': widget.DateWidget(attrs={'class': 'form-control', 'placeholder': 'Lesson Date', 'id': 'kt_datetimepicker_3'}),
            'group': forms.Select(attrs={'class': 'form-control', 'id': 'kt_select2_1'}),
        }


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['lesson', 'student', 'is_present']
        widgets = {
            'lesson': forms.Select(attrs={'class': 'form-control', 'id': 'kt_select1'}),
            'student': forms.Select(attrs={'class': 'form-control', 'id': 'kt_select2'}),
            'is_present': forms.Select(attrs={'class': 'form-control', 'id': 'kt_select3'}),
        }

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['full_name', 'phone', 'email', 'course', 'status']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'course': forms.Select(attrs={'class': 'form-control', 'id': 'kt_select2_1'}),
            'message': widget.CkeditorWidget(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control', 'id': 'kt_select2_2'}),
        }




class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['student', 'group', 'amount', 'date']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control', 'id': 'kt_select2_student'}),
            'group': forms.Select(attrs={'class': 'form-control', 'id': 'kt_select2_group'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = User.objects.filter(role='student')
        self.fields['group'].queryset = Group.objects.all()




class TeacherForm(forms.ModelForm):
    class Meta:
        model = models.Teacher
        fields = [
            "name",
            "last_name",
            "birth_date",
            "address",
            "phone_or_email",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "birth_date": widgets.DateWidget(
                attrs={
                    "class": "form-control",
                    "id": "kt_datetimepicker_3",
                }
            ),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "phone_or_email": forms.TextInput(attrs={"class": "form-control"}),
        }

