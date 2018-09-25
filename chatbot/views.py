from django.shortcuts import render

from django.conf import settings

from django.core.files.storage import FileSystemStorage

import zipfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django import forms
from django.http import HttpResponseRedirect
from codes.Main import *
from .forms import UserRegistrationForm
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
import json
from pathlib import Path


pather = ""
login = False
question = []



@api_view(['GET','POST'])
def get_answer(request):
    if not login:
        return HttpResponseRedirect('/')
    print 'this function is called'
    texter = request.POST.get('question',False);
    print texter
    # answer,pdf_name,page_number  = searchAnswer(texter)
    answer,pdf_name,page_number = 'fileanswer','original_files/music.pdf',2
    # final = [answer,pdf_name,page_number]
    final = answer+"@@@"+pdf_name+"@@@"+str(page_number)
    return HttpResponse(final)

def pdf(request):
    image_data = open("/home/quant/AL/chatbot_demo-master_v3/chatbot/files/original_files/sap.pdf", "rb").read()
    return HttpResponse(image_data, content_type="application/pdf")


def home(request):
    return render(request, 'chatbot/home.html')

def addclient(request):
    if not login:
        return HttpResponseRedirect('/')
    return render(request, 'chatbot/add_client.html')


def signup(request):
    if not login:
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            userObj = form.cleaned_data
            username = userObj['username']
            email =  userObj['email']
            password =  userObj['password']
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, password)
                user = authenticate(username = username, password = password)
                login(request, user)
                return HttpResponseRedirect('/addclient')
            else:
                raise forms.ValidationError('Looks like a username with that email or password already exists')

    else:
        form = UserRegistrationForm()

    return render(request, 'chatbot/signup.html', {'form' : form})





# Login
def connection(request):
    # Redirect to dashboard if the user is log
    if request.user.is_authenticated():
        return redirect('chatbot.views.home')

    # Control if a POST request has been sent.
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None: #Verify form's content existence
            if user.is_active: #Verify validity
                login(request, user)
                login = True
                return redirect('/index') #It's ok, so go to index
            else:
                return redirect('/an_url/') #call the login view

    return render(request, 'login.html', locals())

def viewer(request):
    if not login:
        return HttpResponseRedirect('/')


    without = False

    if request.method == 'POST':

        imp = request.POST['parters']

        print imp
        error_msg = False
        if imp == "1" :

            myfile = request.FILES['myfile']

            fs = FileSystemStorage()

            check = Path("chatbot/files/original_files/"+myfile.name.replace(" ","_"))

            if check.is_file():

                without = "part1"
                error_msg = "Already a file exist in the name"
                return render(request, 'chatbot/startpage.html', { 'parter': without, 'error' :error_msg })


            filename = fs.save("chatbot/files/original_files/"+myfile.name.replace(" ","_"), myfile)
            fs.save("chatbot/static/original_files/"+myfile.name.replace(" ","_"), myfile)

            print "path for the algorithm : " + filename

            pather = filename

            without = "part1"
            error_msg = "File Uploaded"
            return render(request, 'chatbot/startpage.html', { 'parter': without, 'error' :error_msg })

        else:
            print "cool"
            print "all files uploaded "

            # print "except"
            try:
                files('files')
                combineFiles('files')
                error_msg = "processing"
            except:
                print ""
                error_msg = "Error while processing"

            without = "part1"
            return render(request, 'chatbot/startpage.html', { 'parter': without, 'error' :error_msg })


    print "Initial Window"

    without = "part1"

    return render(request, 'chatbot/startpage.html', { 'parter': without })



def viewerclient(request):
    if not login:
        return HttpResponseRedirect('/')


    without = False

    try:
        texter = False
        texter = request.POST.get('texter',False);
        # texter = request.POST['texter']
        if texter :
            print texter,'que'
            # answer,pdf_name,page_number  = searchAnswer(texter)
            answer = 'hsajgkhdjkshgkjdsbvj kjdsbvkedjvjdksb \n hesdgjkns.'  #################33remove later
            answer,pdf_name,page_number = 'hsajgkhdjkshgkjdsbvj kjdsbvkedjvjdksb \n hesdgjkns.'  #################33remove later
            print answer,'answer'
            ans_list = []
            ans_list.append(answer)
        else: ans_list = ['']
        texter = False

    except:
        texter = False
        print 'in except'
        ans_list = ['']

    # print "cool"
    # try :
    #     texter = request.POST['texter']
    #     print texter,'que'
    #     answer = searchAnswer(texter)
    #     print answer,'answer'
    #     ans_list = []
    #     ans_list.append(answer)
    #     # question.append(tp)

    # except :
    #     print "except"


    without = "part2"
    return render(request, 'chatbot/startpageclient.html', { 'parter': without, 'list': ans_list })


# def viewerlogin(request):
