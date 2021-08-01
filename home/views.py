from django.shortcuts import render
from django.http import HttpResponseRedirect
# Create your views here.
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/user/%s"%request.user.username)
    btn_css = 'btn btn-primary'
    join_btn_href = '/user/match_reg'
    if not request.user.is_authenticated:
        join_btn_href = '/user/login'
    return render(request,"home/index.html",return_names('LOGIN','REGISTER',btn_css, btn_css,
    '/user/login', '/user/signup','btn btn-primary btn-lg',join_btn_href, "Join Today's Match",
    cont_us_href='/user/contactus',abt_us_href='/user/aboutus'))

def return_names(LOGIN='',REGISTER='', btn1='', btn2='', href1='', href2='', join_btn_css ='',
    join_btn_href='', join_btn_text='',cont_us_href ='', abt_us_href=''):
    dict = {'LOGIN':LOGIN, 'REGISTER':REGISTER, 'btn1_css':btn1, 'btn2_css':btn2, 'btn1_href':href1,
    'btn2_href':href2,'join_btn_css':join_btn_css, 'join_btn_href':join_btn_href,
     'join_btn_text':join_btn_text,'contactus':cont_us_href,'aboutus':abt_us_href}
    return dict
