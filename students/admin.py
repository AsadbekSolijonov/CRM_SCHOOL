from django.contrib import admin
from students.models import Group, Course, Student, Attendance

admin.site.register([Group, Course, Student, Attendance])
