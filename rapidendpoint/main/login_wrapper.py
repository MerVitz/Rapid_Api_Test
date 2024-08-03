import requests
from .recaptcha import verify_recaptcha
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('onlyfans_login.log')
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

class OnlyFansLoginWrapper:
    def __init__(self, email, password, recaptcha_response, user_agent):
        self.email = email
        self.password = password
        self.recaptcha_response = recaptcha_response
        self.user_agent = user_agent
        self.login_url = 'https://onlyfans.com/api2/v2/users/login'
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': self.user_agent,
            'Origin': 'https://onlyfans.com',
            'Referer': 'https://onlyfans.com/',
            'App-Token': '33d57ade8c02dbc5a333db99ff9ae26a',
            'Sec-Ch-Ua': '"Not)A;Brand";v="99", "Brave";v="127", "Chromium";v="127"',
            'Sec-Ch-Ua-Mobile': '?1',
            'Sec-Ch-Ua-Platform': '"Android"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Gpc': '1',
            'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Accept-Language': 'en-US,en;q=0.5'
        }
        self.cookies = {
            'fp': '067e876a3644d9c0852bc485b340aeda93429aa0',
            'lang': 'en',
            'csrf': 'JCCeUs5bda9610692da88d688b792aa92c4d98dd',
            'st': 'de9aeed1f3fbb3f75aa89effc21c29949ba0a1a2a44d9eed1a47a6bd06241c02',
            'sess': 'k8kjkq3kvia0564bdsp9470v9q',
            '__cf_bm': 'hVmEbDXL7nCg5Nt97qo_ycgl41vj_L2XDmSm8iRCWgc-1722613648-1.0.1.1-HPLv1LUF5EnlBy.XsDtebV5WrvT03sA_M6VGCdZNN_zuMSe9oDFLBlgFSTsb6.50jEifKBNcc49HSjNWraS0EQ',
            '_cfuvid': 'v396uTnmoo5b3Nqn_vXGDqdzsQj_.6ANCjgQGwnmfVA-1722613648848-0.0.1.1-604800000'
        }

    def login(self):
        if not verify_recaptcha(self.recaptcha_response):
            logger.error("reCAPTCHA verification failed!")
            return False, 'reCAPTCHA verification failed!'

        payload = {
            'email': self.email,
            'password': self.password,
            'g-recaptcha-response': self.recaptcha_response,
        }

        logger.debug(f"Sending request to {self.login_url} with payload: {payload} and headers: {self.headers}")

        try:
            response = requests.post(self.login_url, json=payload, headers=self.headers, cookies=self.cookies)
            logger.debug(f"Received response: {response.status_code} - {response.text}")

            if response.status_code == 200:
                return True, 'Login successful!'
            else:
                return False, f'Login failed: {response.text}'
        except Exception as e:
            logger.exception("An error occurred during the login request")
            return False, f'Login failed: {str(e)}'
