from .import views
from django.urls import path

urlpatterns = [
    path('userlist/', views.userlist, name='userlist'),
    path('userdetail/<int:user_id>/', views.userdetail, name='userdetail'),
    path('adduser/', views.adduser, name='adduser'),
    path('edituser/<int:user_id>/', views.edituser, name='edituser'),
    path('deleteuser/<int:user_id>/', views.deleteuser, name='deleteuser'),
]
