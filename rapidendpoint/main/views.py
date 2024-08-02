import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .utils import signinfo_endpoint, OnlyFansAPIWrapper  # Assuming the wrapper is in utils.py or a similar file

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user_agent = request.META['HTTP_USER_AGENT']

        onlyfans = OnlyFansAPIWrapper()
        try:
            login_response = onlyfans.login(email, password)
            request.session['email'] = email
            request.session['password'] = password
            request.session['user_agent'] = user_agent
            request.session['onlyfans_cookies'] = login_response['cookies']  # Store cookies in session if needed
            return redirect('dashboard')
        except requests.exceptions.HTTPError as e:
            return render(request, 'login.html', {'error': str(e)})

    return render(request, 'login.html')

def dashboard_view(request):
    email = request.session.get('email')
    password = request.session.get('password')
    user_agent = request.session.get('user_agent')
    onlyfans_cookies = request.session.get('onlyfans_cookies')

    if not email or not password or not user_agent:
        return redirect('login')

    signinfo_data = signinfo_endpoint(user_agent)

    onlyfans = OnlyFansAPIWrapper()
    try:
        user_details = onlyfans.get_user_details(cookies=onlyfans_cookies)
        context = {
            'email': email,
            'password': password,
            'user_agent': user_agent,
            'signinfo_data': signinfo_data,
            'user_details': user_details
        }
        return render(request, 'dashboard.html', context)
    except requests.exceptions.HTTPError as e:
        return render(request, 'dashboard.html', {'error': str(e)})
