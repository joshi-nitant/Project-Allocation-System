from django.shortcuts import render
from login import forms
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.urls import reverse
from login.models import Site_User
# Create your views here.

def index(request):
    if 'user_id' in request.session:
        return HttpResponseRedirect(reverse('stu_dashboard:dashboard'))

    #login_form = forms.LoginForm()
    if request.method == 'POST':
        return user_login(request)
    else:
        #return render(request,'login/index.html',{'login_form':login_form})
        return render(request,'login/index.html')

def user_login(request):
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username,password=password)

            if user:
                if user.is_active:
                    login(request,user)
                    request.session['user_id'] = user.id
                    return HttpResponseRedirect('dashboard')
                else:
                    return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponseRedirect(reverse('index'))

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
