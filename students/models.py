from django.db import models
from accounts.models import CustomUser
from django.contrib.auth.forms import AuthenticationForm


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Perform login logic here
            pass
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})

class StudentProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE
    )

    registration_number = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    batch = models.IntegerField()
    cgpa = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.user.get_full_name()
    

