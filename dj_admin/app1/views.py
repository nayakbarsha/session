from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm, EditForm, LoginForm
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
# from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
# Create your views here.
def home(request):
    current_user = request.session.get('user')
    search_query = request.GET.get('search', '')  # Get the search query from the URL parameter
    user_list = User.objects.all()
    print("---------------")
    print(len(user_list))
    print(user_list)

    if search_query:
        # If a search query is provided, filter the user list based on username, first name, or last name
        user_list = user_list.filter(Q(username__icontains=search_query) | Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query) | Q(email__icontains=search_query))
    # for paginator
    page = request.GET.get('page', 1)
    paginator = Paginator(user_list, 5)
    
    print(paginator.num_pages)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    if request.user.is_superuser:
        return render(request, 'user_list.html', {'users': users, 'search_query': search_query})
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


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('home')












# from django.db.models import Q

# def home(request):
#     current_user = request.session.get('user')
#     search_query = request.GET.get('search', '')  # Get the search query from the URL parameter
#     user_list = User.objects.all()

#     if search_query:
#         # If a search query is provided, filter the user list based on username, first name, or last name
#         user_list = user_list.filter(Q(username__icontains=search_query) | Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query))

#     page = request.GET.get('page', 1)
#     paginator = Paginator(user_list, 10)
    
#     try:
#         users = paginator.page(page)
#     except PageNotAnInteger:
#         users = paginator.page(1)
#     except EmptyPage:
#         users = paginator.page(paginator.num_pages)
    
#     if request.user.is_superuser:
#         return render(request, 'user_list.html', {'users': users, 'search_query': search_query})
#     elif current_user:
#         param = {'current_user': current_user}
#         return render(request, 'user_list.html', {'users': users, 'search_query': search_query, **param})
#     else:
#         return redirect('login')
# ```

# In this modified `home` view:

# 1. We retrieve the search query from the URL parameter using `request.GET.get('search', '')`.
# 2. If a search query is provided, we filter the `user_list` queryset based on username, first name, or last name using the `Q` object.
# 3. We pass the `search_query` along with the `users` queryset to the `user_list.html` template so that you can display it in the search input field and use it for displaying search results.

# Now, you can update your `user_list.html` template to include the search input field and display the filtered user list.