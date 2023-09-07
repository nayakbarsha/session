from django import forms

class SignupForm(forms.Form):
    firstname = forms.CharField(max_length=20)
    lastname = forms.CharField(max_length=20)
    email = forms.EmailField()
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    mobile = forms.CharField(max_length=10)

class EditForm(forms.Form):
    firstname = forms.CharField(max_length=20)
    lastname = forms.CharField(max_length=20)
    email = forms.EmailField()
    username = forms.CharField(max_length=30)
    mobile = forms.CharField(max_length=10)
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)

class ChangePassword(forms.Form):
    old_password = forms.CharField(max_length=30)
    new_password = forms.CharField(max_length=30)
    confirm_password = forms.CharField(max_length=30)

class OtpValidator(forms.Form):
    mobile = forms.CharField(max_length=10)
    otp = forms.CharField(max_length=6)