from django.shortcuts import render,redirect
from .forms import *
from .models import *
from django.contrib.auth import logout
from django.core.mail import send_mail
from Finalproject import settings
import random
import requests
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    msg=""
    user=request.session.get('user')
    if request.method=='POST': #root
        if request.POST.get('signup')=='signup': #signup
            newuser=signupForm(request.POST)
            if newuser.is_valid():
                username=newuser.cleaned_data.get('username') #code for same username
                try:
                    signupdata.objects.get(username=username)
                    print("Username already exist")
                    msg="Username already exist"
                except signupdata.DoesNotExist: #code for same username
                    newuser.save()
                    print("Signup Successfully!")
                    msg="Signup Successfully!"
            else:
                print(newuser.errors)
                msg="Error..... something went wrong!"

        elif request.POST.get('login')=='login': #login

            unm=request.POST['username']
            pas=request.POST['password']

            user=signupdata.objects.filter(username=unm,password=pas)
            fnm=signupdata.objects.get(username=unm)
            uid=signupdata.objects.get(username=unm)
            print("Firstname:",fnm.firstname)
            print("Current UID:",uid.id)
            if user:
                print("Login successfully!")
                #request.session['user']=unm
                request.session['user']=fnm.firstname
                request.session['uid']=uid.id
                return redirect('notes')
            else:
                print("Error!Login fail.....Try again")
    return render(request,'index.html',{'user':user,'msg':msg})

def about(request):
    return render(request,'about.html')

def contact(request):
    if request.method=='POST':
        fed=contactusForm(request.POST)
        if fed.is_valid():
            fed.save()
            print("Feedback send Successfully!")

            #Email Sending
            otp=random.randint(1111,9999)
            sub="Thank You!"
            msg=f"Dear User!\n\nThanks for your feedback, we will connect shortly!\n\nIf any queries regarding,\n\n Your one time password is {otp}, you can contact us\n\n+91 9724799469 | help@tops-int.com\n\nThanks & Regards!\nTOPS Tech - Rajkot\nwww.tops-int.com"
            from_email=settings.EMAIL_HOST_USER
            #to_email=['kotechamit5@gmail.com','parthhirpara89827@gmail.com','krishnakachhad20@gmail.com','yogitabeladiya2425@gmail.com','rinkalbhad245@gmail.com','janvivora244@gmail.com','vrutikadudhat3@gmail.com','tahjudin597@gmail.com']
            #to_email=['kinnuahir20@gmail.com']
            to_email=[request.POST['email']]
            send_mail(subject=sub,message=msg,from_email=from_email,recipient_list=to_email)
        else:
            print(fed.errors)
    return render(request,'contact.html')

def notes(request):
    user=request.session.get('user')
    if request.method=='POST':
        newnote=notesForm(request.POST, request.FILES)
        if newnote.is_valid():
            newnote.save()
            print("notes successfully!")
        else:
            print(newnote.errors)
    return render(request,'notes.html',{'user':user})

@login_required
def profile(request):
    user=request.session.get('user')
    uid=request.session.get('uid')
    cuser=signupdata.objects.get(id=uid)
    if request.method=='POST':
        updateuser=signupForm(request.POST,instance=cuser)
        if updateuser.is_valid():
            #updateuser=signupForm(request.POST,instance=cuser)
            updateuser.save()
            return redirect('notes')
            print("Profile updated!")
        else:
            print(updateuser.errors)
    return render(request,'profile.html',{'user':user,'cuser':cuser})
    

def userlogout(request):
    logout(request)
    return redirect('/')

def login(request):
    if request.method=='POST':
        unm=request.POST['username']
        pas=request.POST['password']

        user=signupdata.objects.filter(username=unm,password=pas)
        if user: #TRUE
            print("Login Successfull!")
            request.session['user']=unm #create a session
            return redirect('/')
        else:
            print("Error! Login Faild....")
    return render(request,'login.html')
    
