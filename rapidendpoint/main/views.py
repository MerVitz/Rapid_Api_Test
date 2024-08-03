from django.shortcuts import render, redirect
from django.http import JsonResponse
from .login_wrapper import OnlyFansLoginWrapper
import requests
import logging

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# File handler
fh = logging.FileHandler('onlyfans_login_view.log')
fh.setLevel(logging.DEBUG)

# Console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(fh)
logger.addHandler(ch)

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        recaptcha_response = request.POST.get('g-recaptcha-response')
        user_agent = request.META.get('HTTP_USER_AGENT')

        logger.debug(f"Received login request with email: {email}, user_agent: {user_agent}")

        if email and password and recaptcha_response and user_agent:
            wrapper = OnlyFansLoginWrapper(email, password, recaptcha_response, user_agent)
            success, data = wrapper.login()

            if success:
                logger.info("Login successful")
                request.session['onlyfans_cookies'] = data
                request.session['email'] = email
                request.session['user_agent'] = user_agent
                return JsonResponse({'status': 'success', 'message': 'Login successful!'})
            else:
                logger.error(f"Login failed: {data}")
                return JsonResponse({'status': 'error', 'message': data})
        else:
            logger.error("Missing required fields")
            return JsonResponse({'status': 'error', 'message': 'Missing required fields!'})

    return render(request, 'login.html')

def dashboard_view(request):
    email = request.session.get('email')
    onlyfans_cookies = request.session.get('onlyfans_cookies')
    user_agent = request.session.get('user_agent')

    if not email or not onlyfans_cookies:
        return redirect('login')

    onlyfans = OnlyFansAPIWrapper()
    try:
        user_details = onlyfans.get_user_details(cookies=onlyfans_cookies)
        context = {
            'email': email,
            'user_details': user_details
        }
        return render(request, 'dashboard.html', context)
    except requests.exceptions.HTTPError as e:
        logger.error(f"Failed to get user details: {str(e)}")
        return render(request, 'dashboard.html', {'error': f"Failed to get user details: {str(e)}"})
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return render(request, 'dashboard.html', {'error': f"An error occurred: {str(e)}"})
