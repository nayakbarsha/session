from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm

# Create your views here.
def home(request):
    current_user = request.session.get('user')
    
    if current_user:
        param = {'current_user': current_user}
        return render(request, 'base.html', param)
    else:
        return redirect('login')
    # return render(request, 'login.html')


def signup(request):
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
            return HttpResponse('Username already exists.')
        else:
            user = User.objects.create_user(username=username, password=password, first_name=firstname, last_name=lastname, email=email)
            # user.first_name = firstname
            # user.last_name = lastname
            # user.email = email
            user.save()
            return redirect('login')
    else:
        form = SignupForm()
    
    return render(request, 'signup.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')

        user = authenticate(request, username=uname, password=pwd)
        if user is not None:
            login(request, user)
            request.session['user'] = user.username  # Set the user in the session
            return redirect('home')
        else:
            return HttpResponse('Please enter valid Username or Password.')

    return render(request, 'login.html')


def user_logout(request):
    try:
        # removing the user from session
        del request.session['user']
    except KeyError:
        pass
    # logging out the user
    logout(request)
    return redirect('login')























# except:
#         return redirect('login')
#     return redirect('login')




# from django.contrib.auth.decorators import login_required

# @login_required
# def home(request):
#     current_user = request.user.username
#     param = {'current_user': current_user}
#     return render(request, 'base.html', param)




# def home(request):
#     if 'user' in request.session:
#         current_user = request.session['user']
#         param = {'current_user': current_user}
#         return render(request, 'base.html', param)
#     else:
#         return redirect('login')
#     return render(request, 'login.html')













# from django.shortcuts import render, redirect
# from django.contrib.auth import authenticate, login, logout
# from django.http import HttpResponse

# def home(request):
#     if request.user.is_authenticated:
#         current_user = request.user
#         param = {'current_user': current_user}
#         return render(request, 'base.html', param)
#     else:
#         return redirect('login')

# def signup(request):
#     if request.method == 'POST':
#         uname = request.POST.get('uname')
#         pwd = request.POST.get('pwd')
        
#         if User.objects.filter(username=uname).exists():
#             return HttpResponse('Username already exists.')
#         else:
#             user = User.objects.create_user(username=uname, password=pwd)
#             user.save()
#             return redirect('login')
#     else:
#         return render(request, 'signup.html')

# # The login and logout views remain the same as in your original code.

# def logout_view(request):
#     logout(request)
#     return redirect('login')
