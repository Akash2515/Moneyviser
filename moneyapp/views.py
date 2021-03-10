from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from .forms import CreateUForm
def loginUser(request):
    if request.user.is_authenticated:
        return render(request,'dashboard.html')
    else:
        if request.method =="POST":
            username=request.POST.get('username')
            password=request.POST.get('password')
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request, user)
                return render(request,'dashboard.html')

            else:
                messages.info(request,'username or password is incorrect')
        context={}
        return render(request,'Login.html',context)



def registerUser(request):
    form = CreateUForm()
    if request.method=='POST':
        form=CreateUForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Account created' + (form.cleaned_data.get('username')))
            return redirect('login')
    context={ 'form': form }
    return render(request,'Register.html',context)

@login_required(login_url='login')
def home(request):
    context={}
    return render(request,'dashboard.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')