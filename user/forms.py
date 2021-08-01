from django.contrib.auth.models import User
from django import forms
from user.models import order_details, contact_us
import datetime

class login_form(forms.Form):
    username = forms.CharField(
                            widget= forms.TextInput(attrs={'class':'form-input Username',
                            'placeholder':"USERNAME",
                            'required':""}), label = 'Username')
    password = forms.CharField(
                            widget= forms.PasswordInput(attrs={'class':'form-input Password',
                            'placeholder':"PASSWORD",
                            'required':""}), label = 'Password')

class Registration_form(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password']

    first_name= forms.CharField(
                            widget= forms.TextInput(attrs={'class':'form-input',
                            'placeholder':"First Name",
                            'required':"",}), label = '')
    last_name= forms.CharField(
                            widget= forms.TextInput(attrs={'class':'form-input',
                            'placeholder':"Last Name",
                            'required':"",}), label = '')
    username= forms.CharField(
                            widget= forms.TextInput(attrs={'class':'form-input',
                            'placeholder':"Username",
                            'required':"",}), label = '')
    email = forms.EmailField(
                            widget= forms.EmailInput(attrs={'class':'form-input',
                            'placeholder':"Email",
                            'required':"",}), label = '')
    password = forms.CharField(
                            widget= forms.PasswordInput(attrs={'class':'form-input',
                            'placeholder':"Password",
                            'required':"",}), label = '')
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError('Username %s is already in use.' % username)
        return username


class Match_registration(forms.ModelForm):
    class Meta:
        model = order_details
        fields = '__all__'
        widgets = {'date':forms.HiddenInput(), 'order_id': forms.HiddenInput(), 'status':forms.HiddenInput()}

    def return_current_datetime():
        x = datetime.datetime.today().date()
        return x

    name = forms.CharField(widget = forms.TextInput(attrs={'class':'form-input',
                            'placeholder': "Username",
                            'required':''}),label = '')
    in_game_name = forms.CharField(widget = forms.TextInput(attrs={'class':'form-input',
                            'placeholder': "In-Game Name",
                            'required':''}),label = '')
    phone_number = forms.CharField(widget = forms.TextInput(attrs={'class':'form-input',
                            'placeholder': "PHONE NUMBER",
                            'required':''}),label = '')
    date = return_current_datetime()

class Contact_form(forms.ModelForm):
    class Meta:
        model = contact_us
        fields = '__all__'
        widgets = {'status':forms.HiddenInput()}
    from_email = forms.EmailField(
                            widget= forms.EmailInput(attrs={'class':'form-input',
                            'placeholder':"Email",
                            'required':"",}), label = '')
    subject = forms.CharField(
                            widget= forms.TextInput(attrs={'class':'form-input',
                            'placeholder':"Subject",
                            'required':"",}), label = '')
    message = forms.CharField(
                            widget= forms.Textarea(attrs={'class':'form-input',
                            'placeholder':"Enter Your Message Here",
                            'required':"",}), label = '')
