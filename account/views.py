from django.contrib import auth, messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.http import JsonResponse 
from django.views.decorators.csrf import csrf_exempt



from .forms import UserRegistrationForm
from .models import CustomUser

# Create your views here.
def sigin(request):
    if request.method =='POST':
       email = request.POST['email']
       password = request.POST['password']
    
       user = auth.authenticate(request, email=email, password=password)
       
       if user is not None and user.is_active:
           auth.login(request, user)
           return redirect('account:dashboard')
       
       elif user is not None:
           auth.login(request, user)
           return redirect('account:inactive_dashboard')
           
    return render(request, 'account/login.html')


def in_active_dashboard(request):
    context = {
        'info': 'Your Account is currently in active contact the system admin',
        'user': request.user
    }
    return render(request, 'account/in_active_dashboard.html', context)


def dashboard(request):
    return render(request, 'account/dashboard.html')

def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST) # 'request.POST' will contain all the request value
        if form.is_valid():
           user=form.save()
           auth.login(request, user)
           return redirect('account:login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'account/register.html', {'form': form})


def logout(request):
    auth.logout(request)
    return redirect('/')


@csrf_exempt
def authenticate_user_api(request): 
    if request.method == 'POST': 
        username = request.POST.get('username') 
        password = request.POST.get('password') 
        user = authenticate(username=username, password=password) 
        if user is not None: 
            # User is authenticated, allow printing 
            return JsonResponse({'authenticated': True, 'user':user.get_full_name(), 'id':user.id}) 
        
        else: # User is not authenticated, deny printing 
            return JsonResponse({'authenticated': False})

