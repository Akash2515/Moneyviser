from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Customer,Expense,Expense_Split
from .forms import CreateUForm
from django.contrib.sessions.models import Session
from django.core import signing
from collections import defaultdict

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method =="POST":
            username=request.POST.get('username')
            password=request.POST.get('password')
            user=authenticate(request,username=username,password=password)
            if user is not None:
                # request.session['user_id']=ses.custmer_id
                # print(request.session['user_id'])
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
    
    loggedinuser=int(request.user.id)
    
    loggedinuser=loggedinuser-1
   
    for i in Customer.objects.all().filter(custmer_id=loggedinuser):
        displayusername=i.name
        
    value = {}
    for c in Customer.objects.raw('Select name,custmer_id From moneyapp_customer'):
        value[c.custmer_id] = c.name
    
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
        print(expense_info)
        #print(expense_info.objects.get('expense'))
        for i in share_members:
            expense_split_info=Expense_Split(split_amount=split_amount,reciept_id=Customer(custmer_id=i),expense_id=expense_info)
            expense_split_info.save()
    
    return render(request,'dashboard.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')


def Expenselist(request):
    
    safe_value=[]
    value=defaultdict(list)
    context={}
    userloggedin=int(request.user.id)
    userloggedin=userloggedin-1
   
    
    for safe in Expense_Split.objects.all().filter(reciept_id=userloggedin):
        Epk=safe.expense_id.pk
        exp=Expense.objects.filter(pk=Epk).get()
        value['Date']=(exp.Bill_Date)
        value['item']=(exp.item)
        value['Total_amount']=(exp.amount)
        value['amount_split']=(safe.split_amount)
        value['payment_status']=(safe.reciept_paid)
        value['id']=(Epk)
        value=dict(value)
        value_copy=value.copy()
        safe_value.append(value_copy)
    context['safe']=(safe_value)

    if request.method=="POST":
        
        paid_expense_id=request.POST.get('identity')

       
        Expense_Split_update=Expense_Split.objects.get(reciept_id=userloggedin,expense_id=paid_expense_id)
        Expense_Split_update.reciept_paid=True
        Expense_Split_update.save()
        
        Expense_update=Expense.objects.get(pk=paid_expense_id)
        print(Expense_update)
        check_paid_count=Expense_Split.objects.filter(expense_id=paid_expense_id,reciept_paid=True).count()

        for i in Expense.objects.all().filter(expense_id=paid_expense_id):
            length=len(i.split_members)
            
        if length==check_paid_count:
            Expense_update=Expense.objects.get(pk=paid_expense_id)
            Expense_update.paid=True
            Expense_update.save()
        
        
    return render(request,'expense.html',context)


