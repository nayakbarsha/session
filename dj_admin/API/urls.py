from .import views
from django.urls import path

urlpatterns = [
    path('userlist/<int:user_id>', views.userlist, name='userlist'),
]
