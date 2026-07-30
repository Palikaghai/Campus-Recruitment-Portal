from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from placement.models import Company, PlacementDrive
from students.models import StudentProfile


class StudentDrivesTemplateTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="student@example.com",
            email="student@example.com",
            password="StrongPass123",
            first_name="Test",
            last_name="Student",
        )
        self.student_profile = StudentProfile.objects.create(
            user=self.user,
            registration_number="REG-0001",
            department="CSE",
            batch=2026,
            cgpa=8.5,
        )
        self.company = Company.objects.create(
            name="TechCorp",
            location="Bengaluru",
            description="A modern hiring company",
        )
        self.drive = PlacementDrive.objects.create(
            company=self.company,
            job_role="Software Engineer",
            package=12.5,
            location="Remote",
            eligibility_cgpa=7.5,
            description="A great role for ambitious developers.",
            deadline="2030-12-31",
            is_active=True,
        )

    def test_placement_drives_render_detail_links_in_new_tab(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("placement_drives"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'target="_blank"')
        self.assertContains(response, reverse("drive_detail", args=[self.drive.id]))
