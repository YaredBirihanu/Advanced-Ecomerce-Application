from django.shortcuts import render
from .forms import RegistrationForm
from .models import Account

def register(request):
    if request.method=='POST':

        form=RegistrationForm(request.POST)
        if form.is_valid():
            first_name=form.changed_data['first_name']
            last_name=form.changed_data['last_name']
            phone_number=form.changed_data['phone_number']
            email=form.changed_data['email']
            password=form.changed_data['password']
            username=email.split('@')[0]
            user=Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
            user.phone_number=phone_number
            user.save()


        context={
            'form':form,
        }
        return render(request,'accounts/register.html',context)



def login(request):
    return render(request,'accounts/login.html',{})

def logout(request):
    return render(request,'accounts/logout.html',{})

