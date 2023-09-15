from django import forms
from django.contrib.auth.password_validation import validate_password
class SignupForm(forms.Form):
    firstname = forms.CharField(max_length=20)
    lastname = forms.CharField(max_length=20)
    email = forms.EmailField()
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput, validators=[validate_password])

class EditForm(forms.Form):
    firstname = forms.CharField(max_length=20)
    lastname = forms.CharField(max_length=20)
    email = forms.EmailField()
    username = forms.CharField(max_length=30)

    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)

# class ChangePassword(forms.Form):
#     new_password = forms.CharField(widget=forms.PasswordInput, validators=[validate_password])
#     confirm_password = forms.CharField(widget=forms.PasswordInput)

# class ForgotPassword(forms.Form):
#     email = forms.EmailField()
#     username = forms.CharField(max_length=30)

# class OtpValidator(forms.Form):
#     email = forms.EmailField()
#     otp = forms.CharField(max_length=6)