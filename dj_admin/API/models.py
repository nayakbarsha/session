from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.
class Review(models.Model):
    review_user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='reviews')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=200, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "user %s gave " % self.review_user.username + str(self.rating) + "(*)"
        # return "%s the restaurant" % self.place.name
