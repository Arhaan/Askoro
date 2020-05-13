from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    karma_points=models.IntegerField(default=0)
    questions_asked = models.IntegerField(default=0)
    questions_answered = models.IntegerField(default=0)
    verified_email = models.BooleanField(default = False)
    def __str__(self):
        return f"{self.user.username} Profile"
