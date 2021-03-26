from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Customer
from .forms import CreateUForm

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method =="POST":
            username=request.POST.get('username')
            password=request.POST.get('password')
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request, user)
                return redirect('/')

            else:
                messages.info(request,'username or password is incorrect')
        context={}
        return render(request,'safe/Login.html',context)



def registerUser(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form = CreateUForm()
        if request.method=='POST':
            form=CreateUForm(request.POST)
            if form.is_valid():
                form.save()
                customer_info=Customer(name=form.cleaned_data.get('username'),email=form.cleaned_data.get('email'))
                customer_info.save()
                messages.success(request,'Account created' + (form.cleaned_data.get('username')))
                return redirect('login')
        context={ 'form': form }
        return render(request,'safe/Register.html',context)

@login_required(login_url='login')
def home(request):
    value = {}
    for c in Customer.objects.raw('Select name,custmer_id From moneyapp_customer'):
        print('gf',c.name)
        print('id',c.custmer_id)
        value[c.custmer_id] = c.name
    print('value', value)
    context={'value': value}
    if request.method=='POST':
        item=request.POST.get('itemname')
        paidBy=request.POST.get('paiduser')
        amount=request.POST.get('amount')
        share_members=request.POST.get('recipientId')

        print(paidBy)
        print(share_members)


    return render(request,'dashboard.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')


