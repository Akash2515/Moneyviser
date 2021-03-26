from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Customer,Expense,Expense_Split
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
        itemdetail=request.POST.get('itemname')
        paidBy=int(request.POST.get('PaidUser'))
        amount=int(request.POST.get('amount'))
        share_members=request.POST.getlist('recipientId')
        share_members=[int(i) for i in share_members]
        members_count=len(share_members)
        split_amount=(int(amount))/members_count
        expense_info=Expense(item=itemdetail,no_of_splits=members_count,split_members=share_members,amount=amount,author_id=Customer(custmer_id=paidBy))
        expense_info.save()

    return render(request,'dashboard.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')


