import pickle
from pprint import pprint

with open('cookies.pkl', 'rb') as f:
    cookies = pickle.load(f)
    print("Cookies:")
    pprint(cookies, indent=4)




# import requests
# import pickle

# with open('cookies.pkl', 'rb') as file:
#     cookies = pickle.load(file)

# cookies_dict = {cookie['name']: cookie['value'] for cookie in cookies}

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
#     "Content-Type": "application/json",
#     "Accept": "application/json, text/plain, */*",
#     "App-Token": "33d57ade8c02dbc5a333db99ff9ae26a",
#     "Origin": "https://onlyfans.com",
#     "Referer": "https://onlyfans.com/"
# }

# #The new endpoint wrapper.
# response = requests.get('https://onlyfans.com/api2/v2/users/me', headers=headers, cookies=cookies_dict)

# print(response.json())
