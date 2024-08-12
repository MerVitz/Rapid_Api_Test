import json
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback
from requests.cookies import RequestsCookieJar
"""
This file is working corrctly weel and good, even in terms of logging details 
and flow of conetnt but there is some capabilty


"""


# Initialize Chrome with DevTools Protocol enabled
chrome_options = Options()
chrome_options.add_argument("--auto-open-devtools-for-tabs")
chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

# Path to your ChromeDriver
service = Service('D:\My_Dependencies\chromedriver-win64\chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to OnlyFans login page
driver.get("https://onlyfans.com")
time.sleep(5)  # Allow some time for the page to load

def capture_network_logs():
    logs = driver.get_log('performance')
    request_headers = {}
    response_headers = {}
    request_payload = {}
    request_cookies = []
    response_cookies = []
    all_cookies = driver.get_cookies()

    for entry in logs:
        log = json.loads(entry['message'])['message']
        if log['method'] == 'Network.requestWillBeSent':
            if log['params']['request']['url'] == "https://onlyfans.com/api2/v2/users/login":
                request_headers = log['params']['request']['headers']
                request_payload = log['params']['request']['postData'] if 'postData' in log['params']['request'] else {}
                with open('request_headers.json', 'w') as f:
                    json.dump(request_headers, f, indent=4)
                with open('request_payload.json', 'w') as f:
                    json.dump(request_payload, f, indent=4)
                print("Request headers and payload details saved successfully.")
        if log['method'] == 'Network.responseReceived':
            if log['params']['response']['url'] == "https://onlyfans.com/api2/v2/users/login":
                response_headers = log['params']['response']['headers']
                with open('response_headers.json', 'w') as f:
                    json.dump(response_headers, f, indent=4)
                print("Response headers saved successfully.")
    
    # Split cookies into request and response cookies
    for cookie in all_cookies:
        if cookie['domain'] == '.onlyfans.com':
            request_cookies.append(cookie)
        else:
            response_cookies.append(cookie)

    # Save request cookies
    with open('request_cookies.json', 'w') as f:
        json.dump(request_cookies, f, indent=4)
    print("Request cookies saved successfully.")

    # Save response cookies
    with open('response_cookies.json', 'w') as f:
        json.dump(response_cookies, f, indent=4)
    print("Response cookies saved successfully.")

def interactable(driver, by, value, wait_time=40):
    try:
        element = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((by, value))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        element = WebDriverWait(driver, wait_time).until(
            EC.element_to_be_clickable((by, value))
        )
        return element
    except Exception as e:
        print(f"Error finding element: {by}={value} - {e}")
        return None

def check_recaptcha():
    logs = driver.get_log('performance')
    for entry in logs:
        log = json.loads(entry['message'])['message']
        if log['method'] == 'Network.requestWillBeSent':
            url = log['params']['request']['url']
            if "recaptcha" in url:
                return True
    return False

try:
    # Wait for the email field to be present
    email_field = interactable(driver, By.NAME, 'email')
    if not email_field:
        raise Exception("Email field not found.")

    # Wait for the password field to be present
    password_field = interactable(driver, By.NAME, 'password')
    if not password_field:
        raise Exception("Password field not found.")

    print("Please enter your email and password in the browser window and press Enter here.")
    input("Press Enter after entering your email and password...")

    # Automatically click the login button
    login_button = interactable(driver, By.XPATH, '//button[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "log in")]')
    if not login_button:
        login_button = interactable(driver, By.CSS_SELECTOR, 'button.g-btn.m-rounded.m-block.m-md.mb-0')

    if login_button and login_button.is_displayed() and login_button.is_enabled():
        driver.execute_script("arguments[0].click();", login_button)
        print("Login button clicked. Checking for reCAPTCHA challenge...")
    else:
        raise Exception("Login button not interactable.")

    # Check for reCAPTCHA challenge
    if check_recaptcha():
        print("reCAPTCHA challenge detected. Please solve the CAPTCHA manually.")
        input("Press Enter after solving the CAPTCHA...")

        # Try to click the login button again after CAPTCHA is solved
        login_button = interactable(driver, By.XPATH, '//button[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "log in")]')
        if not login_button:
            login_button = interactable(driver, By.CSS_SELECTOR, 'button.g-btn.m-rounded.m-block.m-md.mb-0')
        if login_button and login_button.is_displayed() and login_button.is_enabled():
            driver.execute_script("arguments[0].click();", login_button)
            print("Login button clicked again after CAPTCHA.")
        else:
            raise Exception("Re-located login button not clickable.")

    # Wait for login to complete
    while "https://onlyfans.com/my" not in driver.current_url and driver.execute_script("return document.readyState") != "complete":
        print("Waiting for login to complete...")
        time.sleep(5)

    if "https://onlyfans.com/" in driver.current_url:
        print("Login successful")
        
        # Allow time for network logs to be captured
        time.sleep(10)

        # Capture and save network logs
        capture_network_logs()

    else:
        print("Login failed or still pending.")

except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
finally:
    driver.quit()

# Convert cookies to RequestsCookieJar format
def format_cookies(cookies_list):
    """ Convert Selenium cookies to a format suitable for requests. """
    jar = RequestsCookieJar()
    for cookie in cookies_list:
        jar.set(cookie['name'], cookie['value'], domain=cookie.get('domain', ''), path=cookie.get('path', '/'))
    return jar

# Automatic request to get payout details
def get_payout_details():
    # Load the extracted details
    try:
        with open('request_cookies.json', 'r') as file:
            request_cookies_list = json.load(file)
    except FileNotFoundError:
        print("Request cookies file not found.")
        return

    try:
        with open('response_cookies.json', 'r') as file:
            response_cookies_list = json.load(file)
    except FileNotFoundError:
        print("Response cookies file not found.")
        return

    try:
        with open('request_headers.json', 'r') as file:
            request_headers = json.load(file)
    except FileNotFoundError:
        print("Request headers file not found.")
        return

    # Convert cookies to RequestsCookieJar format
    request_cookies = format_cookies(request_cookies_list)
    response_cookies = format_cookies(response_cookies_list)

    # Extract necessary details from headers and cookies
    auth_id = next((cookie['value'] for cookie in response_cookies_list if cookie['name'] == 'auth_id'), '')
    sess = next((cookie['value'] for cookie in request_cookies_list if cookie['name'] == 'sess'), '')
    useragent = request_headers.get("User-Agent", "")
    xbc = request_headers.get("xbc", "")
    sign = request_headers.get("sign", "")
    sign_parts = sign.split(':') if sign else ['', '', '', '']
    signstart = sign_parts[0]
    signend = sign_parts[-1]

    # Create querystring
    querystring = {
        "auth_id": auth_id,
        "sess": sess,
        "useragent": useragent,
        "xbc": xbc,
        "timezone": "America/Los_Angeles",
        "apptoken": request_headers.get("apptoken", ""),
        "signstart": signstart,
        "signend": signend
    }

    # Set the RapidAPI headers
    rapidapi_headers = {
        "x-rapidapi-key": "29e990d324msh007d44b2549955bp136713jsn7489cfc5b4f2",
        "x-rapidapi-host": "onlyfans.p.rapidapi.com"
    }

    # Check if all necessary querystring parameters are present
    if not all(querystring.values()):
        print("Missing querystring parameters.")
        print(f"Querystring: {querystring}")
        return

    # Construct the payout request URL
    url = "https://onlyfans.p.rapidapi.com/users/payouts"

    # Send the request to the payout endpoint
    try:
        response = requests.get(url, headers=rapidapi_headers, cookies=request_cookies, params=querystring)
        if response.status_code == 200:
            print("Request sent to payout endpoint successfully.")
            print(response.json())
        else:
            print(f"Request failed with status code {response.status_code}: {response.text}")
    except requests.RequestException as e:
        print(f"Error sending request: {e}")

get_payout_details()


