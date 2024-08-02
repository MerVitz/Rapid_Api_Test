import requests

def signinfo_endpoint(user_agent):
    url = "https://onlyfans.p.rapidapi.com/signinfo/"
    api_key = "29e990d324msh007d44b2549955bp136713jsn7489cfc5b4f2"

    querystring = {"useragent": user_agent}
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "onlyfans.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json() if response.status_code == 200 else {}

class OnlyFansAPIWrapper:
    def __init__(self):
        self.base_url = "https://onlyfans.com/api2/v2/users/me"
        self.session = requests.Session()

    def login(self, email, password):
        login_url = f"{self.base_url}/users/login"
        payload = {
            "email": email,
            "encodedPassword": password
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "App-Token": "33d57ade8c02dbc5a333db99ff9ae26a",
            "Origin": "https://onlyfans.com",
            "Referer": "https://onlyfans.com/"
        }

        response = self.session.post(login_url, json=payload, headers=headers)

        if response.status_code == 200:
            cookies = self.session.cookies.get_dict()
            return {"status": "success", "cookies": cookies}
        else:
            response.raise_for_status()

    def get_user_details(self, cookies):
        user_details_url = f"{self.base_url}/users/me"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "App-Token": "33d57ade8c02dbc5a333db99ff9ae26a"
        }

        for key, value in cookies.items():
            self.session.cookies.set(key, value)

        response = self.session.get(user_details_url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()
