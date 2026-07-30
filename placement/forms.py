from django import forms
from students.models import StudentProfile
from recruiters.models import RecruiterProfile
from placement.models import Company, PlacementDrive
from accounts.models import CustomUser


class StudentEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))

    class Meta:
        model = StudentProfile
        fields = ["registration_number", "department", "batch", "cgpa", "skills", "resume"]
        widgets = {
            "registration_number": forms.TextInput(attrs={"class": "form-control"}),
            "department": forms.TextInput(attrs={"class": "form-control"}),
            "batch": forms.NumberInput(attrs={"class": "form-control"}),
            "cgpa": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "skills": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "resume": forms.FileInput(attrs={"class": "form-control"}),
        }


class AddRecruiterForm(forms.Form):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "First Name"}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Last Name"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "recruiter@company.com"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Password"}))
    company_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Company Name"}))
    designation = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "HR Manager / Talent Acquisition"}))
    company_website = forms.URLField(required=False, widget=forms.URLInput(attrs={"class": "form-control", "placeholder": "https://company.com"}))


class CompanyApprovalForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ["name", "website", "email", "location", "is_approved", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "website": forms.URLInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "is_approved": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
