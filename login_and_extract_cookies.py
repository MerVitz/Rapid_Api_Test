from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback
import time
import pickle

# Set up WebDriver (adjust the path to your WebDriver)
service = Service('D:\\chromedriver-win64\\chromedriver.exe')
driver = webdriver.Chrome(service=service)

# Navigate to OnlyFans login page
driver.get('https://onlyfans.com')

# Wait for the page to load
time.sleep(10)  # Increased the initial wait time

# Define a function to ensure element is interactable
def interactable(driver, by, value, wait_time=40):
    element = WebDriverWait(driver, wait_time).until(
        EC.presence_of_element_located((by, value))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    element = WebDriverWait(driver, wait_time).until(
        EC.element_to_be_clickable((by, value))
    )
    return element

try:
    # Ensure the page has fully loaded by waiting for a known element
    WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.NAME, 'email'))
    )
    print("Page loaded successfully.")

    # Find and fill the email field using JavaScript
    email_field = interactable(driver, By.NAME, 'email')
    print("Email field found and interactable.")
    driver.execute_script("arguments[0].value = arguments[1];", email_field, 'valentinlazo2000@gmail.com')

    # Find and fill the password field using JavaScript
    password_field = interactable(driver, By.NAME, 'password')
    print("Password field found and interactable.")
    driver.execute_script("arguments[0].value = arguments[1];", password_field, 'PapiLazo2000!')

    # Debug: Print all button elements and their classes on the page
    buttons = driver.find_elements(By.TAG_NAME, 'button')
    for button in buttons:
        print(f"Button text: {button.text}, Classes: {button.get_attribute('class')}")

    # Attempt to find the login button using case-insensitive XPath
    try:
        login_button = interactable(driver, By.XPATH, '//button[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "log in")]', wait_time=40)
        print("Login button found and clickable using XPath.")
    except Exception as e:
        print("XPath method failed, falling back to CSS selector.")
        # Print the page source for debugging
        with open("page_source.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)
        login_button = interactable(driver, By.CSS_SELECTOR, 'button.g-btn.m-rounded.m-block.m-md.mb-0', wait_time=40)
    
    # Ensure the login button is visible and enabled before clicking
    if login_button.is_displayed() and login_button.is_enabled():
        print("Login button is displayed and enabled.")
        driver.execute_script("arguments[0].click();", login_button)
    else:
        print("Login button is not interactable.")

    # Wait for user to solve CAPTCHA manually if it appears
    print("Please solve the CAPTCHA manually in the opened browser window if it appears.")
    while "https://onlyfans.com/my" not in driver.current_url:
        print("Waiting for login to complete...")
        time.sleep(5)  # Check every 5 seconds

    # Check if logged in successfully
    if "https://onlyfans.com/my" in driver.current_url:
        print("Login successful")

        # Extract cookies
        cookies = driver.get_cookies()
        
        # Save cookies to a file
        with open('cookies.pkl', 'wb') as file:
            pickle.dump(cookies, file)
    else:
        print("Login failed")
except Exception as e:
    print(f"An error occurred: {e}")
    traceback.print_exc()
finally:
    # Close the browser
    driver.quit()
