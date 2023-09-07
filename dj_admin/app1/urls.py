from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('edit/<int:user_id>/', views.edit, name='edit'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    # path('change_password/', views.change_password, name='change_password'),
]
