from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404

handler404 = 'app1.views.custom_404'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('app1.urls')),
    path('api/',include('API.urls')),
    path('api-auth/', include('rest_framework.urls')),
    # path('verification/', include('verify_email.urls')),
]
