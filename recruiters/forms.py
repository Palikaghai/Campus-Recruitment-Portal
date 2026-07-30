from django import forms
from placement.models import Company, PlacementDrive
from interviews.models import Interview


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ["name", "website", "email", "location", "logo", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Company Name"}),
            "website": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://company.com"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "careers@company.com"}),
            "location": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Bangalore, Remote"}),
            "logo": forms.FileInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "About the company..."}),
        }


class PlacementDriveForm(forms.ModelForm):
    class Meta:
        model = PlacementDrive
        fields = [
            "company",
            "job_role",
            "package",
            "location",
            "eligibility_cgpa",
            "deadline",
            "description",
            "is_active",
        ]
        widgets = {
            "company": forms.Select(attrs={"class": "form-select"}),
            "job_role": forms.TextInput(attrs={"class": "form-control", "placeholder": "Software Engineer, Product Analyst, etc."}),
            "package": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "placeholder": "Package in LPA (e.g. 12.50)"}),
            "location": forms.TextInput(attrs={"class": "form-control", "placeholder": "Job Location"}),
            "eligibility_cgpa": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "placeholder": "Minimum CGPA required (e.g. 7.5)"}),
            "deadline": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "Role responsibilities, requirements, selection process..."}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class InterviewScheduleForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = [
            "interview_type",
            "interview_date",
            "interview_time",
            "mode",
            "meeting_link",
            "venue",
            "interviewer",
        ]
        widgets = {
            "interview_type": forms.Select(attrs={"class": "form-select"}),
            "interview_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "interview_time": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "mode": forms.Select(attrs={"class": "form-select"}),
            "meeting_link": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://meet.google.com/xyz (Online mode)"}),
            "venue": forms.TextInput(attrs={"class": "form-control", "placeholder": "Auditorium / Block 3 (Offline mode)"}),
            "interviewer": forms.TextInput(attrs={"class": "form-control", "placeholder": "Interviewer Name / Panel"}),
        }
