from django.db import models
from django.db.models import Count

from config.settings import AUTH_USER_MODEL


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Course(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f"{self.name}"


class Group(TimeStampedModel):
    name = models.CharField(max_length=150, help_text="Guruh nomi...", unique=True)
    course = models.ForeignKey(Course, related_name='groups', on_delete=models.RESTRICT)
    teacher = models.ForeignKey(AUTH_USER_MODEL, related_name='courses', on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=250, blank=True, null=True)

    def __str__(self):
        return f"{self.name}({self.teacher.username})"


class Student(TimeStampedModel):
    STATUS_CHOICES = (
        ('active', 'Qatnashmoqda'),
        ('sick', 'Kasal'),
        ('freeze', 'Muzlatilgan'),
        ('on_trip', 'Safarda'),
        ('other', 'Boshqa')
    )
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    parent_phone = models.CharField(max_length=12)
    other_phone = models.CharField(max_length=12, blank=True, null=True)
    date_of_bith = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    groups = models.ManyToManyField(Group, related_name='students')

    def __str__(self):
        groups = ", ".join([gp.name for gp in self.groups.all()])
        return F"{self.first_name}({groups}, {self.status}, {self.parent_phone})"

    class Meta:
        ordering = ['-created_at']  # [Z-A]

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class Attendance(models.Model):
    PRESENT = 'present'
    ABSENT = 'absent'
    STATUS_CHOICES = [
        (PRESENT, 'Present'),
        (ABSENT, 'Absent'),
    ]

    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    note = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        unique_together = ('student', 'group', 'date')

    def __str__(self):
        return f"{self.date} - {self.student}: {self.status} - {self.note}"
