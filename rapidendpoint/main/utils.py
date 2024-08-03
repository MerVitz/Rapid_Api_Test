# import requests
# import logging

# logger = logging.getLogger(__name__)

# class OnlyFansAPIWrapper:
#     def __init__(self):
#         self.base_url = "https://onlyfans.com/api2/v2"
#         self.session = requests.Session()

#     def login(self, email, password):
#         login_url = f"{self.base_url}/users/login"
#         payload = {
#             "email": email,
#             "password": password
#         }
#         headers = {
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
#             "Content-Type": "application/json",
#             "Accept": "application/json, text/plain, */*",
#             "App-Token": "33d57ade8c02dbc5a333db99ff9ae26a",
#             "Origin": "https://onlyfans.com",
#             "Referer": "https://onlyfans.com/"
#         }

#         response = self.session.post(login_url, json=payload, headers=headers)

#         if response.status_code == 200:
#             cookies = self.session.cookies.get_dict()
#             return {"status": "success", "cookies": cookies}
#         else:
#             logger.error(f"Login failed: {response.status_code} - {response.text}")
#             response.raise_for_status()

#     def get_user_details(self, cookies):
#         user_details_url = f"{self.base_url}/users/me"
#         headers = {
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
#             "Accept": "application/json, text/plain, */*",
#             "App-Token": "33d57ade8c02dbc5a333db99ff9ae26a"
#         }

#         for key, value in cookies.items():
#             self.session.cookies.set(key, value)

#         response = self.session.get(user_details_url, headers=headers)

#         if response.status_code == 200:
#             return response.json()
#         else:
#             logger.error(f"Get user details failed: {response.status_code} - {response.text}")
#             response.raise_for_status()
