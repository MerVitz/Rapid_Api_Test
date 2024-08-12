import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def check_recaptcha(driver):
    """
    Check if a reCAPTCHA challenge is detected in the network logs.
    Args:
        driver (webdriver.Chrome): The Selenium WebDriver instance.
    Returns:
        bool: True if reCAPTCHA challenge is detected, False otherwise.
    """
    logs = driver.get_log('performance')
    for entry in logs:
        log = json.loads(entry['message'])['message']
        if log['method'] == 'Network.requestWillBeSent':
            url = log['params']['request']['url']
            if any(keyword in url for keyword in ["recaptcha/enterprise/reload", "recaptcha/enterprise/anchor"]):
                return True
    return False

def check_login_success(driver):
    """
    Check if login was successful by inspecting network logs.
    Args:
        driver (webdriver.Chrome): The Selenium WebDriver instance.
    Returns:
        bool: True if login is successful, False otherwise.
    """
    logs = driver.get_log('performance')
    for entry in logs:
        log = json.loads(entry['message'])['message']
        if log['method'] == 'Network.responseReceived':
            if log['params']['response']['url'] == "https://onlyfans.com/api2/v2/users/me":
                return True
    return False

def interactable(driver, by, value, wait_time=40):
    """
    Wait for an element to be interactable.
    Args:
        driver (webdriver.Chrome): The Selenium WebDriver instance.
        by (By): Locator strategy (e.g., By.NAME, By.XPATH).
        value (str): Locator value.
        wait_time (int): Time to wait for the element to be interactable.
    Returns:
        WebElement: The interactable WebElement if found, None otherwise.
    """
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
