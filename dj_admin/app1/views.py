from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm, EditForm, LoginForm
from .helpers import send_forgot_password_mail
from django. contrib import messages 
import uuid

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
    # print("Inside signup")
    errors = []
    if request.method == 'POST':
        # print("Inside Post")
        form = SignupForm(request.POST)
        if form.is_valid():
            # print("Form is Valid")
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
        else:
            print(form.errors)
            print("Oppps....Form is Invalid!")
            # errors = ['form invalid']
            return render(request, 'signup.html', {'signup_form': form, 'errors': errors})
        # print(uname, pwd)
        # DB validation for duplicate user
        try:
            # errors = []
            # if User.objects.filter(username=username).exists() and User.objects.filter(email=email).exists() :
            #     errors.append('Username already exists.')
            #     errors.append('Email already exists.')
            # elif User.objects.filter(email=email).exists():
            #     errors.append('Email already exists.')
            # elif User.objects.filter(username=username).exists():
            #     errors.append('Username already exists.')
            # else:
            #     user = User.objects.create_user(username=username, password=password,
            #          first_name=firstname, last_name=lastname, email=email)
            #     user.save()
            #     return redirect('login')
            isDuplicate = False
            errors = []
            if User.objects.filter(email=email).exists():
                isDuplicate = True
                errors.append('Email already exists.')
            if User.objects.filter(username=username).exists():
                isDuplicate = True
                errors.append('Username already exists.')
            if not isDuplicate:
                user = User.objects.create_user(username=username, password=password,
                     first_name=firstname, last_name=lastname, email=email)
                user.save()
                return redirect('login')
        except Exception as e:
            print("Exception Happened {e}")
    else:
        # print("Showing signup Form")
        form = SignupForm()

    # print("Before Final line")
    return render(request, 'signup.html', {'signup_form': form, 'errors' : errors}) 



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
    errors = []
    if request.user.is_authenticated:
        user = User.objects.get(id=user_id)
        if request.method == 'POST':
            form = EditForm(request.POST)
            if form.is_valid():
                user.first_name = form.cleaned_data['firstname']
                user.last_name = form.cleaned_data['lastname']
                user.email = form.cleaned_data['email']
                user.username = form.cleaned_data['username']
            else:
                print(form.errors)
                print("Oppps....Form is Invalid!")
                # errors = ['Form invalid']
                return render(request,'edit.html', {'edit_form': form, 'errors': errors})
            
            isDuplicate = False
            errors = []
            if User.objects.exclude(id=user_id).filter(username=user.username).exists():
                isDuplicate = True
                errors.append('Username already exists.')
            if User.objects.exclude(id=user_id).filter(email=user.email).exists():
                isDuplicate = True
                errors.append('Email already exists.')
            if not isDuplicate:
                user.save()
                return redirect('home')
        else:
            form = EditForm({'firstname': user.first_name, 'lastname': user.last_name,
                    'email': user.email, 'username': user.username})
    else:
        return redirect('login')
    return render(request,'edit.html', {'edit_form': form, 'errors': errors})


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
    
def custom_404(request, exception):
    return render(request, '404.html', status=404)

# def custom_500(request):
#     return render(request, '500.html', status=500)

def change_password(request, token):
    context = {}

    try:
        profile_obj = User.objects.filter(forgot_password_token = token).exists
        print(profile_obj)    
    except Exception as e:
        print(e)
    return render(request,'change_password.html')

def forgot_password(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')

            if not User.objects.filter(username=username).exists():
                messages.success(request, 'no user found with this username')
                return redirect('/forgot_password/')
            
            user_obj = User.objects.get(username=username)
            token = str(uuid.uuid4())
            profile_obj = User.objects.get(user=user_obj)
            profile_obj.forgot_password_token = token
            profile_obj.save()
            send_forgot_password_mail(user_obj, token)
            messages.success(request, 'An e-mail has been sent to your email id')
            return redirect('/forgot_password/')
        
    except Exception as e:
        print(e)
    return render(request, 'forgot_password.html')