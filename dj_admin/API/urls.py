from .import views
from django.urls import path

urlpatterns = [
    path('userlist/', views.UserList.as_view(), name='userlist'),
    path('createuser/', views.CreateUser.as_view(), name='createuser'),
    path('userdetails/<int:pk>/', views.Userdetails.as_view(), name='userdetail'),
    path('reviewlist/',views.ReviewList.as_view(), name='reviewlist'),
    path('givereview/',views.CreateReview.as_view(), name='reviewlist'),
    path('reviewdetails/<int:pk>/', views.ReviewDetails.as_view(), name='reviewdetails'),
    # path('login/', obtain_auth_token)
    path('login/', views.LoginView.as_view()),

    # path('adduser/', views.adduser, name='adduser'),
#     path('edituser/<int:user_id>/', views.edituser, name='edituser'),
#     path('deleteuser/<int:user_id>/', views.deleteuser, name='deleteuser'),
]
