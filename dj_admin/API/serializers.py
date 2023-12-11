from rest_framework import serializers
from django.contrib.auth.models import User
from API.models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        # fields = "__all__"
        exclude = ["created_at", "updated_at"]

class UserlistSerializer(serializers.ModelSerializer):
    # reviews = serializers.StringRelatedField(read_only=True)
    reviews = ReviewSerializer(read_only=True)
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "reviews"]
        # fields = '__all__'