
from django.contrib.auth import views as auth_views


from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('application/edit/<int:pk>/', views.edit_application, name='edit_application'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('recruiter-dashboard/', views.recruiter_dashboard, name='recruiter_dashboard'),
]
