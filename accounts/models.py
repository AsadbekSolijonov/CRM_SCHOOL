from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=9, unique=True,
                             help_text="Hamma nomer +998 dan boshlanadi va 9 ta uzunlikda qabul qilinadi.")
    REQUIRED_FIELDS = ['email', 'phone']

    def __str__(self):
        return f"{self.username}"


