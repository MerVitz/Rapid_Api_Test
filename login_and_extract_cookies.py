from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback
import time
import pickle

# Initialize the WebDriver
service = Service('D:\My_Dependencies\chromedriver-win64\chromedriver.exe')
driver = webdriver.Chrome(service=service)

# Navigate to OnlyFans login page
driver.get('https://onlyfans.com')
time.sleep(5)  # Allow some time for the page to load

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

    # Wait for user input to proceed
    input("Press Enter after entering your email and password...")

    # Automatically click the login button
    login_button = interactable(driver, By.XPATH, '//button[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "log in")]')
    if not login_button:
        login_button = interactable(driver, By.CSS_SELECTOR, 'button.g-btn.m-rounded.m-block.m-md.mb-0')

    if login_button and login_button.is_displayed() and login_button.is_enabled():
        driver.execute_script("arguments[0].click();", login_button)
        print("Login button clicked. Please solve the CAPTCHA manually if it appears.")
    else:
        raise Exception("Login button not interactable.")

    # Wait for user to solve CAPTCHA
    input("Press Enter after solving the CAPTCHA (if it appears)...")

    # Try to click the login button again after CAPTCHA is solved
    try:
        login_button = interactable(driver, By.XPATH, '//button[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "log in")]')
        if not login_button:
            login_button = interactable(driver, By.CSS_SELECTOR, 'button.g-btn.m-rounded.m-block.m-md.mb-0')
        if login_button and login_button.is_displayed() and login_button.is_enabled():
            driver.execute_script("arguments[0].click();", login_button)
            print("Login button clicked again after CAPTCHA.")
    except:
        print("Re-located login button not clickable, it might not be necessary.")

    # Wait for login to complete
    while "https://onlyfans.com/my" not in driver.current_url and driver.execute_script("return document.readyState") != "complete":
        print("Waiting for login to complete...")
        time.sleep(5)

    if "https://onlyfans.com/" in driver.current_url:
        print("Login successful")

        # Save cookies to a file
        cookies = driver.get_cookies()
        with open('cookies.pkl', 'wb') as file:
            pickle.dump(cookies, file)
        print("Cookies saved successfully.")
    else:
        print("Login failed or still pending.")

except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
finally:
    driver.quit()
