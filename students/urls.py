from django.urls import path
from students import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('employee/', views.employee, name='employee'),
    path('groups/', views.groups, name='groups'),
    path('events/', views.events, name='events'),
]
