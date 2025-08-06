from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        TEACHER = 'TEACHER', 'Teacher'
        STUDENT = 'STUDENT', 'Student'

    phone = models.CharField(max_length=9, unique=True,
                             help_text="Hamma nomer +998 dan boshlanadi va 9 ta uzunlikda qabul qilinadi.")
    base_role = Role.ADMIN
    role = models.CharField(max_length=20, choices=Role.choices)
    REQUIRED_FIELDS = ['email', 'phone']

    def __str__(self):
        return f"{self.username}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
        super().save(*args, **kwargs)


class StudentManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return queryset.filter(role=CustomUser.Role.STUDENT)


class Student(CustomUser):
    base_role = CustomUser.Role.STUDENT

    student = StudentManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Faqat studentlar uchun."


class TeacherManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        return queryset.filter(role=CustomUser.Role.TEACHER)


class Teacher(CustomUser):
    base_role = CustomUser.Role.TEACHER

    teacher = TeacherManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Faqat ustozlar uchun."


class TeacherProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    teacher_id = models.IntegerField(null=True, blank=True)


@receiver(post_save, sender=Teacher)
def create_teacher_profile(sender, instance, created, **kwargs):
    if created and instance.role == CustomUser.Role.TEACHER:
        TeacherProfile.objects.create(user=instance)


class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    student_id = models.IntegerField(null=True, blank=True)


@receiver(post_save, sender=Student)
def create_student_profile(sender, instance, created, **kwargs):
    if created and instance.role == CustomUser.Role.STUDENT:
        StudentProfile.objects.create(user=instance)
