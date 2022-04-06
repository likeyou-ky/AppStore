from cgitb import html
from sre_constants import SUCCESS
from urllib import request
from django.shortcuts import render
from django.core.mail import send_mail # for mail send we need to import it
from django.shortcuts import render, redirect
from django.db import connection
from django.http import HttpResponse
from django.http import JsonResponse
import pymysql
# Create your views here.

def logout(request):
    try:
        del request.session['your-email']
    except KeyError:
        pass
    result_dict = {}
    result_dict['logout_success'] = 'See you next time! You have sucessfuly logged out'
    return render(request, 'home.html', result_dict)

def mainpage(request):
    if 'your-email' not in request.session:
        if request.method == "POST":
            email = request.POST['your-email']
            password = request.POST['your-password']
            if email!='' and password!='':
                verification = "SELECT * FROM users WHERE your_email = '" + email + "' AND password = '" + password + "';"
                c = connection.cursor()
                c.execute(verification)
                account_exist = c.fetchall()    
                results_dict = {}
                if not account_exist:
                    results_dict = {'error':'Please try again. Entered username or password is wrong. Please sign up if you have not done so.'}
                    return render(request, 'login.html',results_dict)
                request.session['your-email'] = email
                query = "SELECT your_email, display_name, age, phone_number, vaccination_status, rating, count_rate FROM users WHERE your_email = '" + request.session['your-email'] + "';"
            else:
                return render(request, 'login.html')
        else:
            return render(request, 'login.html')
    else:
        query = "SELECT your_email, display_name, age, phone_number, vaccination_status, rating, count_rate FROM users WHERE your_email = '" + request.session['your-email'] + "';"
    c = connection.cursor()
    c.execute(query)
    results = c.fetchall()
    result_dict = {'records': results}
    return render(request, 'mainpage.html', result_dict)

def login(request):
    signup = {}#####
    if request.method == "POST":
        display_photo = request.POST['your-photo']
        display_name = request.POST['your-name']
        email = request.POST['your-email']
        age = request.POST['your-age']
        phone_number = request.POST['phone-number']
        gender = request.POST['your-gender']
        vaccination_status = request.POST['your-vaccination']
        password = request.POST['your-password']
        
        if display_photo!= '' and  display_name != '' and email != '' and age !='' and phone_number !='' and gender !='' and vaccination_status !='' and password !='':
            email_check =  "SELECT * FROM users WHERE your_email = '" + email + "';"
            c = connection.cursor()
            c.execute(email_check)
            emails_exist = c.fetchall() #container
            results_dict = {}
            if len(display_name)>128:
                results_dict['name_warning'] = 'Your name cannot be more than 128 characters'
            if len(email) > 128:
                results_dict['email_verifier'] = ' Your email cannot be more than 128 characters'
            elif emails_exist:
                results_dict['email_verifier']='There is already an account with email ' + email
            if len(password) < 6:
                results_dict['pw_warning'] = 'Your password cannot be less than 6 characters'
            elif len(password) >64:
                results_dict['pw_warning'] = 'Your password cannot be more than 64 characters'
            if results_dict:
                return render(request,'booknow.html',results_dict)
        insert_query = "INSERT INTO users (display_photo, display_name, your_email, age, phone_number, gender, vaccination_status, password, rating, count_rate) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');" % (display_photo, display_name,email,age,phone_number,gender,vaccination_status,password,0,0)
        c = connection.cursor()
        c.execute(insert_query)
        signup['signupconfirm'] = "You have successfully signed up, proceed to log in."  ###########
    return render(request, 'login.html', signup)

def contact(request):
    return render(request, 'contact.html')

def signup_confirmation(request):
    return render(request, 'signup_confirmation.html')

def about(request):
    return render(request, 'about.html', {})

def update(request):
    return render(request, 'update.html')

def update_success(request):
    if request.method == "POST":
        email = request.session['your-email']
        display_photo = request.POST['profile_photo']
        phone_number = request.POST['phone-number']
        password = request.POST['your-password']
        if display_photo!= '' and phone_number!='' and password!='':
            update_user =  "UPDATE users SET display_photo = '%s', phone_number='%s', password='%s' WHERE your_email = '%s'" % (display_photo,phone_number,password,email)
            c = connection.cursor()
            c.execute(update_user)
    return render(request, 'update_success.html')

def booknow(request):
    return render(request, 'booknow.html')

def home(request): 
    return render(request, 'home.html', {})

def settings(request):
	return render(request, 'settings.html')

def settings_success(request):
	return render(request, 'settings_success.html')

def result(request): # edit here to add sql for search function
    if  request.GET.get('name',''):
        search_string = request.GET.get('name','')
    elif request.GET.get('price',''):
        search_string = request.GET.get('price','')
    elif request.GET.get('genre',''):
        search_string = request.GET.get('genre','')
    return render(request, 'result.html',{})

def ratings(request):
    return render(request, 'ratings.html')

def rate_success(request):
    if request.method == "POST":
        error={}
        rater = request.session['your-email']
        being_rated = request.POST['rate-email']
        score = request.POST['rating']
        check = "SELECT * FROM users WHERE your_email = '" + being_rated + "';"
        c = connection.cursor()
        c.execute(check)
        valid = c.fetchall()
        if being_rated == rater:
            error['rateyourself'] = 'You cannot rate yourself'
            return render(request, 'ratings.html', error)
        if not valid:
            error['ratenotfound'] = 'The email of the person you are trying to rate is not found in our database'
            return render(request, 'ratings.html', error)
        else:
            query = "SELECT count_rate FROM users WHERE your_email = '" + being_rated + "';"
            query2 = "SELECT rating FROM users WHERE your_email = '" + being_rated + "';"
            c.execute(query)
            count_rate = c.fetchall()[0][0]
            count_rate = float(count_rate)+1
            c.execute(query2)
            rating = c.fetchall()[0][0]
            rating = float(rating)+float(score)
            query3= "UPDATE users SET rating = '%s', count_rate='%s' WHERE your_email = '%s'" % (rating/count_rate,count_rate,being_rated)
            c.execute(query3)
            return render(request, 'rate_success.html')
    return render(request, 'rate_success.html')
