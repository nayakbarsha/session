from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register the built-in User model with UserAdmin
admin.site.unregister(User)  # Unregister the default User admin
admin.site.register(User, UserAdmin)  # Register with UserAdmin to get enhanced admin features
