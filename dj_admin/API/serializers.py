from rest_framework import serializers
from django.contrib.auth.models import User

class UserlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]