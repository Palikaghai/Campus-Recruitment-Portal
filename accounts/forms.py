from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class BaseRegistrationForm(UserCreationForm):

    class Meta:
        model = CustomUser

        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "phone_number",
            "password1",
            "password2",
        ]
class StudentRegistrationForm(BaseRegistrationForm):

    def save(self, commit=True):

        user = super().save(commit=False)

        user.role = "student"

        if commit:
            user.save()

        return user
class RecruiterRegistrationForm(BaseRegistrationForm):

    company_name = forms.CharField(max_length=150)

    designation = forms.CharField(max_length=100)

    def save(self, commit=True):

        user = super().save(commit=False)

        user.role = "recruiter"

        if commit:
            user.save()

        return user
class OfficerRegistrationForm(BaseRegistrationForm):

    employee_id = forms.CharField(max_length=20)

    department = forms.CharField(max_length=100)

    def save(self, commit=True):

        user = super().save(commit=False)

        user.role = "placement_officer"

        if commit:
            user.save()

        return user
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):

    class Meta:
        model = CustomUser

        fields = [
            "username",
            "password",
        ]