from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm, EditForm, LoginForm
# Create your views here.
def home(request):
    current_user = request.session.get('user')
    # print(current_user)
    if request.user.is_superuser:
        users = User.objects.all()
        # print(users)
        param = {'users': users}
        return render(request, 'user_list.html', param)
    elif current_user:
        param = {'current_user': current_user}
        # print(current_user)
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
        if User.objects.filter(email=email).exists():
            message = 'Email already exists.'
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
    # if user is not authenticated or not logged in yet show them login page
    if not request.user.is_authenticated:
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
            else:
                message = 'Please enter valid Username or Password.'
    # else they are already loggedin so we should show them loggedin page or homepage as we call it
    else:
        return redirect('home')
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

def edit(request, user_id):
    message = ''
    if request.user.is_authenticated:
        user = User.objects.get(id=user_id)
        if request.method == 'POST':
            form = EditForm(request.POST)
            if form.is_valid():
                user.first_name = form.cleaned_data['firstname']
                user.last_name = form.cleaned_data['lastname']
                user.email = form.cleaned_data['email']
                user.username = form.cleaned_data['username']
            if User.objects.exclude(id=user_id).filter(username=user.username).exists():
                message = 'Username already exists.'
            if User.objects.exclude(id=user_id).filter(email=user.email).exists():
                message = 'Email already exists.'
            else:
                user.save()
                return redirect('home')
        else:
            form = EditForm({'firstname': user.first_name, 'lastname': user.last_name,
                    'email': user.email, 'username': user.username})
    else:
        return redirect('login')
    return render(request,'edit.html', {'edit_form': form, 'message' : message})


def delete_user(request, user_id):
    current_user = request.session.get('user')
    if request.user.is_superuser:
        user = User.objects.get(id=user_id)
        user.delete()
        # logout(request)
        return redirect('home')
    elif current_user:
        user = User.objects.get(id=user_id)
        user.delete()
        return redirect('login')
    else:
        return redirect('login')

# def change_password(request, user_id):
#     if request.user.is_authenticated:
#         user = User.objects.get(id=user_id)
#         if request.method == 'POST':
#             form = EditForm(request.POST)
#     return render(request,'change_password.html', {'change_password': form})
