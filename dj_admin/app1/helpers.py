from django.core.mail import send_mail
from django.conf import settings

def send_forgot_password_mail(email, token):
    subject = 'Link to reset Password'
    message = f'Hi, Click on the link to reset password http://127.0.0.1.8000/change_password/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True