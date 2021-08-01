from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from user import forms
from django.http import HttpResponseRedirect
from user.models import order_details
from django.views.decorators.csrf import csrf_exempt
from paytm import Checksum
import datetime
import random
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError
MERCHANT_KEY = 'wGO25AMYdUp64WnV'

def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/user/%s'%request.user.username)
    login_form = forms.login_form()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        authentication = authenticate(username = username, password =  password)
        if authentication is not None:
            if authentication.is_active:
                request.session.set_expiry(86400)
                login(request, authentication)
                return HttpResponseRedirect('/user/%s'%request.user.username)
    return render(request,'registration/login.html',return_names(login_form,'LOGIN','REGISTER',
    'btn btn-primary','btn btn-primary','/user/login', '/user/signup'))

def profile_login(request, username=None):
    url_username = username #sending username to index page to toggle Register button
    try:
        User.objects.get(username=url_username)
    except:
        return HttpResponseRedirect('/')
    try:
        person = order_details.objects.all
        for per in person:
            if person.status == False:
                order_details.objects.get(name=url_username).delete()
    except:
        pass
    try:
        join_btn_css1 = 'btn btn-primary btn-lg'
        join_btn_text1 = "Join Today's Match"
        join_btn_href1 = '/user/match_reg'
        person = order_details.objects.filter(date=datetime.datetime.today().date()).get(name=url_username)
        if person.status == True:
            join_btn_css1 = 'btn btn-primary btn-lg disabled'
            join_btn_text1 = 'SUCCESSFULLY REGISTERED'
            join_btn_href1 = ''
        if person.status == False:
            order_details.objects.get(name=url_username).delete()
    except:
        pass
    return render(request,'home/index.html',return_names(LOGIN='PAYMENT HISTORY', btn1='btn btn-primary',
    href1='/user/paymenthistory', REGISTER=('LOGOUT %s'%url_username),btn2='btn btn-primary', href2 ='/accounts/logout',
    join_btn_css = join_btn_css1, join_btn_text=join_btn_text1, join_btn_href = join_btn_href1 , cont_us_href='/user/contactus',abt_us_href='/user/aboutus'))

def user_signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/user/%s'%request.user.username)
    signup_form = forms.Registration_form()
    if request.method == 'POST':
        signup_form = forms.Registration_form(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            user.set_password(user.password)
            user.save()
            authentication = authenticate(username = user.username, password =  user.password)
            if authentication is not None:
                if authentication.is_active:
                    request.session.set_expiry(86400)
                    login(request, authentication)
            return HttpResponseRedirect('/home')

    return render(request, 'registration/signup.html',return_names(signup_form,'LOGIN','REGISTER',
    'btn btn-primary','btn btn-primary','/user/login', '/user/signup', cont_us_href='/user/contactus',abt_us_href='/user/aboutus'))



@csrf_exempt
def join_match(request):
    register_match_form = forms.Match_registration()
    if request.method == 'POST':
        register_match_form = forms.Match_registration(request.POST)
        if register_match_form.is_valid():
            register_match_form.save(commit=True)
        def order_id():
            id = random.randint(1111,9999)
            id2 = random.randint(1111,9999)
            id3 = random.randint(1111,9999)
            return str(id),str(id2),str(id3)
        id4, id5, id6 = order_id()
        order_id = id4+id5+id6

        confirm_order_details = order_details.objects.get(name = request.POST['name'])
        confirm_order_details.status = False
        confirm_order_details.order_id = order_id
        confirm_order_details.save()

        param_dict =  {
                'MID':'ppaONS13342711553446',
                'ORDER_ID':order_id,
                'TXN_AMOUNT':'10',
                'CUST_ID':'email',
                'INDUSTRY_TYPE_ID':'Retail',
                'WEBSITE':'DEFAULT',
                'CHANNEL_ID':'WEB',
                'CALLBACK_URL':'http://127.0.0.1:8000/user/handlerequest/'
        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict,MERCHANT_KEY)
        return render(request, 'payment/paytm.html', {'param_dict' : param_dict})
    return render(request, 'registration/join_match.html', return_names(register_match_form,
    LOGIN='PAYMENT HISTORY',btn1='btn btn-primary', REGISTER=('LOGOUT %s'%request.user.username),
    btn2='btn btn-primary', href2 ='/accounts/logout', cont_us_href='/user/contactus',abt_us_href='/user/aboutus'))

def set_payment_status(var_order_id):
    confirm_order_details = order_details.objects.get(order_id = var_order_id)
    confirm_order_details.status = True
    confirm_order_details.save()

@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    checksum = '1'
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    if checksum == '1':
        return HttpResponseRedirect('/home')
    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
            set_payment_status(response_dict['ORDERID'])
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return HttpResponseRedirect('/home')

def paymenthistory(request):
    person_order_history = order_details.objects.filter(name=request.user.username)
    return render(request, 'payment/paymenthistory.html',return_names(LOGIN='PAYMENT HISTORY', btn1='btn btn-primary',
    href1='/user/paymenthistory', REGISTER=('LOGOUT %s'%request.user.username),btn2='btn btn-primary',href2 ='/accounts/logout',extra=person_order_history,
     cont_us_href='/user/contactus',abt_us_href='/user/aboutus'))


def aboutus(request):
    btn_css = 'btn btn-primary'
    register = 'REGISTER'
    login = 'LOGIN'
    href1 = '/user/login'
    href2 = '/user/signup'
    if request.user.is_authenticated:
        register = ('LOGOUT %s'%request.user.username)
        login = 'PAYMENT HISTORY'
        href1 = '/user/paymenthistory'
        href2 = '/accounts/logout'
    return render(request, 'home/aboutus.html',return_names(LOGIN=login,REGISTER=register,btn1=btn_css, btn2=btn_css,
    href1=href1, href2=href2, cont_us_href='/user/contactus',abt_us_href='/user/aboutus'))

def contactus(request):
    form = forms.Contact_form()
    btn_css = 'btn btn-primary'
    register = 'REGISTER'
    login = 'LOGIN'
    href1 = '/user/login'
    href2 = '/user/signup'
    if request.user.is_authenticated:
        register = ('LOGOUT %s'%request.user.username)
        login = 'PAYMENT HISTORY'
        href1 = '/user/paymenthistory'
        href2 = '/accounts/logout'
    if request.method == 'POST':
        form = forms.Contact_form(request.POST)
        if form.is_valid():
            form.save(commit=True)
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, ('Sorry for The inconvinience . Your Query with subject "%s" is Submitted . Our Team will Contact You with in 24 hrs'%subject), from_email, ['princegoyal49@gmail.com'],fail_silently=False)
                return render(request, 'home/thanks.html',return_names(LOGIN=login,REGISTER=register,btn1=btn_css, btn2=btn_css,
                href1=href1, href2=href2, cont_us_href='/user/contactus',abt_us_href='/user/aboutus'))
            except BadHeaderError:
                pass
    return render(request, 'home/contactus.html',return_names(FORM=form,LOGIN=login,REGISTER=register,btn1=btn_css, btn2=btn_css,
    href1=href1, href2=href2, cont_us_href='/user/contactus',abt_us_href='/user/aboutus'))

def return_names(FORM='', LOGIN='',REGISTER='', btn1='', btn2='', href1='', href2='', join_btn_css ='',
    join_btn_href='', join_btn_text='',extra='',cont_us_href ='', abt_us_href=''):
    dict = {'form':FORM, 'LOGIN':LOGIN, 'REGISTER':REGISTER, 'btn1_css':btn1, 'btn2_css':btn2,
    'btn1_href':href1, 'btn2_href':href2, 'join_btn_css':join_btn_css, 'join_btn_href':join_btn_href,
     'join_btn_text':join_btn_text, 'extra':extra, 'contactus':cont_us_href,'aboutus':abt_us_href}
    return dict
