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
    c.execute('''SELECT u.display_photo, u.display_name, u.age, u.gender, 
            b.height, b.rate_per_hour, b.interest_1, b.education, 
            u.vaccination_status, u.phone_number, u.rating
            FROM users u, buddies b
            WHERE u.your_email = b.your_email
            ORDER BY u.rating DESC LIMIT 5''')
    toprated = c.fetchall()
    c.execute('''SELECT i.interest, u.rating
            FROM users u, buddies b, interests i
            WHERE u.your_email = b.your_email
            AND u.rating >= (
                SELECT AVG(u1.rating)
                FROM users u1, buddies b1
                WHERE u1.your_email = b1.your_email)
            AND i.interest IN (SELECT interest FROM (
                SELECT b.interest_1 AS interest, COUNT(b.interest_1) FROM buddies b
                GROUP BY b.interest_1
                HAVING COUNT(b.interest_1)>=ALL(
                SELECT COUNT(b1.interest_1) FROM buddies b1
                GROUP BY b1.interest_1)
                UNION
                SELECT b.interest_2 AS interest, COUNT(b.interest_2) FROM buddies b
                GROUP BY b.interest_2
                HAVING COUNT(b.interest_2)>=ALL(
                SELECT COUNT(b1.interest_2) FROM buddies b1
                GROUP BY b1.interest_2)
                UNION
                SELECT b.interest_3 AS interest, COUNT(b.interest_3) FROM buddies b
                GROUP BY b.interest_3
                HAVING COUNT(b.interest_3)>=ALL(
                SELECT COUNT(b1.interest_3) FROM buddies b1
                GROUP BY b1.interest_3)
                UNION
                SELECT b.interest_4 AS interest, COUNT(b.interest_4) FROM buddies b
                GROUP BY b.interest_4
                HAVING COUNT(b.interest_4)>=ALL(
                SELECT COUNT(b1.interest_4) FROM buddies b1
                GROUP BY b1.interest_4)
                UNION
                SELECT b.interest_5 AS interest, COUNT(b.interest_5) FROM buddies b
                GROUP BY b.interest_5
                HAVING COUNT(b.interest_5)>=ALL(
                SELECT COUNT(b1.interest_5) FROM buddies b1
                GROUP BY b1.interest_5)) AS cte) 
                ORDER BY u.rating
                LIMIT 5;''')
    trendyhobby = c.fetchall()
    result_dict = {'records': results, 'toprated': toprated, 'trendyhobby': trendyhobby}
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
            if len(display_name)>64:
                results_dict['name_warning'] = 'Your name cannot be more than 64 characters'
            if len(email) > 128:
                results_dict['email_verifier'] = ' Your email cannot be more than 128 characters'
            elif emails_exist:
                results_dict['email_verifier'] = 'There is already an account with email ' + email
            if phone_number[0] != '8' and phone_number[0] != '9':
                results_dict['phone_verifier'] = 'You have entered an invalid Singapore phone number'
            if len(password) < 6:
                results_dict['pw_warning'] = 'Your password cannot be less than 6 characters'
            elif len(password) > 64:
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
    if request.method == "POST":
        email = request.session['your-email']
        height = request.POST['height']
        education = request.POST['education']
        rate_per_hour = request.POST['rate_per_hour']
        interest1 = request.POST['interest1']
        interest2 = request.POST['interest2']
        interest3 = request.POST['interest3']
        interest4 = request.POST['interest4']
        interest5 = request.POST['interest5']

        c = connection.cursor()
        c.execute("SELECT * FROM buddies WHERE your_email = '" + email + "';")
        valid = c.fetchall()
        if not valid:
            c.execute("INSERT INTO buddies VALUES ('{0}',{1},'{2}',{3},'{4}','{5}','{6}','{7}','{8}');".format(email, height, education, rate_per_hour, interest1, interest2, interest3, interest4, interest5))
        else:
            update_height = (lambda x: "height = " + str(height) if len(x)!=0 else "")(height)
            update_education = (lambda x: "education = '" + education + "'" if len(x)!=0 else "")(education)
            update_rate = (lambda x : "rate_per_hour = " + str(rate_per_hour) if len(x)!=0 else "")(rate_per_hour)
            interest1 = (lambda x: "interest_1 = '" + interest1 + "'" if len(x)!=0 else "")(interest1)
            interest2 = (lambda x: "interest_2 = '" + interest2 + "'"if len(x)!=0 else "")(interest2)
            interest3 = (lambda x: "interest_3 = '" + interest3 + "'"if len(x)!=0 else "")(interest3)
            interest4 = (lambda x: "interest_4 = '" + interest4 + "'"if len(x)!=0 else "")(interest4)
            interest5 = (lambda x: "interest_5 = '" + interest5 + "'"if len(x)!=0 else "")(interest5)
            parameters = ','.join([update_height, update_education, update_rate, interest1, interest2, interest3, interest4, interest5])
            c.execute("UPDATE buddies SET "+parameters+" WHERE your_email = '"+email+"';")
    return render(request, 'settings_success.html')

def result(request): # edit here to add sql for search function
    if request.method == "GET":
        gender = request.GET.get('gender', '')
        age_range = request.GET.get('age_range', '')
        min_rate = request.GET.get('min_rate', '')
        max_rate = request.GET.get('max_rate', '')
        interest = request.GET.get('interest', '')
        min_age = 18
        max_age = 130
        
        if min_rate == '':
            min_rate = 0
        if max_rate == '':
            max_rate = 1000000
        if age_range != '':
            min_age = int(age_range[:2])
            if min_age != 60:
                max_age = int(age_range[-2:])
        
        c = connection.cursor()
        if gender != '' and interest != '':
            c.execute('''
            SELECT u.display_photo, u.display_name, u.age, u.gender, 
            b.height, b.rate_per_hour, b.interest_1, b.education, 
            u.vaccination_status, u.phone_number, u.rating
            FROM users u, buddies b, interest i
            WHERE u.your_email = b.your_email
            AND u.gender = %s
            AND u.age >= %s AND u.age <= %s 
            AND b.rate_per_hour >= %s AND b.rate_per_hour <= %s
            AND (b.interest_1 = %s OR b.interest_2 = %s OR b.interest_3 = %s OR b.interest_4 = %s OR b.interest_5 = %s)
            ORDER BY u.rating DESC;
            ''',[gender, min_age, max_age, min_rate, max_rate, interest, interest, interest, interest, interest])
            results = c.fetchall()
        elif gender != '' and interest == '':
            c.execute('''
            SELECT u.display_photo, u.display_name, u.age, u.gender, 
            b.height, b.rate_per_hour, b.interest_1, b.education, 
            u.vaccination_status, u.phone_number, u.rating
            FROM users u, buddies b
            WHERE u.your_email = b.your_email
            AND u.gender = %s
            AND u.age >= %s AND u.age <= %s 
            AND b.rate_per_hour >= %s AND b.rate_per_hour <= %s
            ORDER BY u.rating DESC;
            ''',[gender, min_age, max_age, min_rate, max_rate])
            results = c.fetchall()
        elif gender == '' and interest != '':
            c.execute('''
            SELECT u.display_photo, u.display_name, u.age, u.gender, 
            b.height, b.rate_per_hour, b.interest_1, b.education, 
            u.vaccination_status, u.phone_number, u.rating
            FROM users u, buddies b
            WHERE u.your_email = b.your_email
            AND u.age >= %s AND u.age <= %s 
            AND b.rate_per_hour >= %s AND b.rate_per_hour <= %s
            AND (b.interest_1 = %s OR b.interest_2 = %s OR b.interest_3 = %s OR b.interest_4 = %s OR b.interest_5 = %s)
            ORDER BY u.rating DESC;
            ''',[min_age, max_age, min_rate, max_rate, interest, interest, interest, interest, interest])
            results = c.fetchall()
        else:
            c.execute('''
            SELECT u.display_photo, u.display_name, u.age, u.gender, 
            b.height, b.rate_per_hour, b.interest_1, b.education, 
            u.vaccination_status, u.phone_number, u.rating
            FROM users u, buddies b
            WHERE u.your_email = b.your_email
            AND u.age >= {0} AND u.age <= {1} 
            AND b.rate_per_hour >= {2} AND b.rate_per_hour <= {3}
            ORDER BY u.rating DESC;
            '''.format(str(min_age), str(max_age), str(min_rate), str(max_rate)))
            results = c.fetchall()
        result_dict = {'records': results}
    return render(request, 'result.html', result_dict)

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
            p = float(count_rate)-1
            rating = (float(rating)*p)+float(score)
            query3= "UPDATE users SET rating = '%s', count_rate='%s' WHERE your_email = '%s'" % (rating/count_rate,count_rate,being_rated)
            c.execute(query3)
            return render(request, 'rate_success.html')
    return render(request, 'rate_success.html')
