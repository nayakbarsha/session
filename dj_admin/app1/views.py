from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from . import forms 
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm, EditForm, LoginForm

# Create your views here.
def home(request):
    current_user = request.session.get('user')
    print(current_user)
    if request.user.is_superuser:
        users = User.objects.all()
        param = {'users': users}
        return render(request, 'user_list.html', param)
    elif current_user:
        param = {'current_user': current_user}
        return render(request, 'user_list.html', param)
    else:
        return redirect('login')


def signup(request):
    message = ''
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
        # print(uname, pwd)
        if User.objects.filter(username=username).exists():
            message = 'Username already exists.'

        else:
            user = User.objects.create_user(username=username, password=password,
                     first_name=firstname, last_name=lastname, email=email)
            # user.first_name = firstname
            # user.last_name = lastname
            # user.email = email
            user.save()
            return redirect('login')
    else:
        form = SignupForm()
    
    return render(request, 'signup.html', {'signup_form': form, 'message' : message})



def user_login(request):
    form = LoginForm()
    message = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['user'] = user.username  # Set the user in the session
            return redirect('home')
        if not User.objects.filter(username=username).exists():
            message = 'User does not exists.'
            # return redirect('login')
        else:
            message = 'Please enter valid Username or Password.'
            # return redirect('login')
    return render(request, 'login.html', context={'login_form': form, 'message' : message})


def user_logout(request):
    try:
        # removing the user from session
        del request.session['user']
    except KeyError:
        pass
    # logging out the user
    logout(request)
    return redirect('login')

def edit(request):
    user = request.user
    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['firstname']
            user.last_name = form.cleaned_data['lastname']
            user.email = form.cleaned_data['email']
            user.save()
            return redirect('home')
    else:
        form = EditForm({'firstname': user.first_name, 'lastname': user.last_name, 'email': user.email})
    return render(request,'edit.html', {'edit_form': form}) 


def delete_user(request):
    user = request.user
    user.delete()
    logout(request)
    return redirect('login')

