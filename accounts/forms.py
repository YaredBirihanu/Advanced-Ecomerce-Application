from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter password',
        #'class': 'form-control',
        # 'type': 'password',
        # 'id': 'password'
    }))
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm password',
        #'class': 'form-control',
        # 'type': 'password',
        # 'id': 'confirm_password'
        }))
    
    class Meta:
        model = Account
        fields =['first_name','last_name','email','password','phone_number']


    def __init__(self,*args,**kwargs):
        super(RegistrationForm,self).__init__(self,*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder']='Enter first name'
        self.fields['last_name'].widget.attrs['placeholder']='Enter last name'
        self.fields['phone_number'].widget.attrs['placeholder']='Enter phone number'
        self.fields['email'].widget.attrs['placeholder']='Enter email'
       
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
