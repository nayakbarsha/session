from .import views
from django.urls import path

urlpatterns = [
    path('createstudent/',views.create_student, name='createstudent'),
]

