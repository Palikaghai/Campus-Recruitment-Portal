from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

        self.fields["first_name"].widget.attrs["placeholder"] = "First Name"
        self.fields["last_name"].widget.attrs["placeholder"] = "Last Name"
        self.fields["username"].widget.attrs["placeholder"] = "Username"
        self.fields["email"].widget.attrs["placeholder"] = "Email"
        self.fields["phone_number"].widget.attrs["placeholder"] = "Phone Number"
        self.fields["password1"].widget.attrs["placeholder"] = "Password"
        self.fields["password2"].widget.attrs["placeholder"] = "Confirm Password"


class StudentRegistrationForm(BaseRegistrationForm):

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "student"

        if commit:
            user.save()

        return user


class RecruiterRegistrationForm(BaseRegistrationForm):

    company_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Company Name"
        })
    )

    designation = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Designation"
        })
    )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "recruiter"

        if commit:
            user.save()

        return user


class OfficerRegistrationForm(BaseRegistrationForm):

    employee_id = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Employee ID"
        })
    )

    department = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Department"
        })
    )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = "placement_officer"

        if commit:
            user.save()

        return user


class LoginForm(AuthenticationForm):

    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Email",
            }
        ),
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter Password",
            }
        )
    )