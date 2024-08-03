from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
import time

# Initialize Chrome with DevTools Protocol enabled
chrome_options = Options()
chrome_options.add_argument("--auto-open-devtools-for-tabs")
chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

# Path to your ChromeDriver
service = Service('D:\\chromedriver-win64\\chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to OnlyFans login page
driver.get("https://onlyfans.com")
time.sleep(5)  # Allow some time for the page to load

# Function to capture network logs
def capture_network_logs():
    logs = driver.get_log('performance')
    for entry in logs:
        log = json.loads(entry['message'])['message']
        if log['method'] == 'Network.requestWillBeSent':
            if log['params']['request']['url'] == "https://onlyfans.com/api2/v2/users/login":
                with open('request_details.json', 'w') as f:
                    json.dump(log['params']['request'], f, indent=4)
                print("Request details saved successfully.")
        if log['method'] == 'Network.responseReceived':
            if log['params']['response']['url'] == "https://onlyfans.com/api2/v2/users/login":
                with open('response_details.json', 'w') as f:
                    json.dump(log['params']['response'], f, indent=4)
                print("Response details saved successfully.")

# Wait for the user to manually input their email, password, and solve the CAPTCHA
print("Please enter your email, password, and solve the CAPTCHA in the browser window.")
input("Press Enter after entering your email, password, and solving the CAPTCHA...")

# Automatically click the login button
login_button = driver.find_element(By.XPATH, '//button[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "log in")]')
driver.execute_script("arguments[0].click();", login_button)

# Check for the presence of reCAPTCHA
def is_recaptcha_present():
    try:
        driver.find_element(By.CLASS_NAME, "g-recaptcha")
        return True
    except:
        return False

# Wait for reCAPTCHA to be solved
while is_recaptcha_present():
    print("Waiting for reCAPTCHA to be solved...")
    time.sleep(5)

# Attempt to click the login button again after solving reCAPTCHA
login_button = driver.find_element(By.XPATH, '//button[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "log in")]')
driver.execute_script("arguments[0].click();", login_button)

# Wait for login to complete
while "https://onlyfans.com/me" not in driver.current_url and driver.execute_script("return document.readyState") != "complete":
    print("Waiting for login to complete...")
    time.sleep(5)

if "https://onlyfans.com/" in driver.current_url:
    print("Login successful")

    # Capture and save network logs
    capture_network_logs()

    # Allow some time to verify the network logs have been saved
    time.sleep(10)  # Adjust the sleep time as needed
else:
    print("Login failed or still pending.")

driver.quit()
