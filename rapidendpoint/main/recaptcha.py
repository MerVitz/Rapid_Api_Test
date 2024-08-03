import requests
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('onlyfans_recaptcha.log')
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

def verify_recaptcha(recaptcha_response):
    secret_key = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'
    payload = {
        'secret': secret_key,
        'response': recaptcha_response
    }

    logger.debug(f"Verifying reCAPTCHA with payload: {payload}")

    try:
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
        result = response.json()
        logger.debug(f"reCAPTCHA response: {result}")
        return result.get('success')
    except Exception as e:
        logger.exception("An error occurred during reCAPTCHA verification")
        return False
