import requests

url = "https://onlyfans.p.rapidapi.com/signinfo/"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
api_key = "29e990d324msh007d44b2549955bp136713jsn7489cfc5b4f2"

querystring = {"useragent": user_agent}
headers = {
    "x-rapidapi-key": api_key,
    "x-rapidapi-host": "onlyfans.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())
