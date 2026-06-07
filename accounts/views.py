from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm , RegisterForm
from .models import UserRole
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User

# Register View
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data.get('role')
            user.is_staff = role != 'PATIENT'
            user.save()
            UserRole.objects.create(
                user=user,
                role=role
            )
            login(request, user)
            return redirect('dashboard')
        
    else:
        form = RegisterForm()
            
    return render(
        request,
        'accounts/register.html',
        {'form':form}
    )

# Login View
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')

    else:
        form = LoginForm()

    return render(
        request,
        'accounts/login.html',
        {'form': form}
    )
        
        
@login_required
@require_POST
def logout_view(request):
    logout(request)
    return redirect('login')


