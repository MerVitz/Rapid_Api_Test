import requests

#Endpoin found being used, in login.
url = "https://onlyfans.com/api2/v2/users/login"

#Headers o the payload
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "Accept": "application/json, text/plain, */*",
    "App-Token": "33d57ade8c02dbc5a333db99ff9ae26a",
    "Cookie": "_cfuvid=h.vKRxv_LEAd1UEuuWwmZgya56FkalXBtXgZqkyq07I-1722537001444-0.0.1.1-604800000; fp=9a82335d20268a3b462b3c635b9d206a2f49889b; lang=en; sess=s51geqvaq1ku33urm7rslf7sdd; csrf=HcvrD0F1fbc70110e2fa84365af6a1f021b90316",
    "Origin": "https://onlyfans.com",
    "Referer": "https://onlyfans.com/",
    "Sign": "27421:04b9aee7d8844156eac7f4e25fb0b00f9340dd60:927:66abb0b7",
    "Time": "1722537167586",
    "X-BC": "9a82335d20268a3b462b3c635b9d206a2f49889b",
    "X-Hash": "JPJ0HnlUE+T4f+ectnzRQ2oS0V2TA5f/ssmQJQw="
}

payload = {
    "email": "valentinlazo2000@gmail.com",
    "e-recaptcha-response": "03AFcWeA65lB3OpmIAlrP6XEhxzPj4THakRnl0JhDwisxotSRSrz0Dnn1IYUkePuexjvpStvrYIBLgEe5R7BbYc5sz6ZTov31yMFIJvpeMRSEAut_5PjVupuolEUjJloXjuei8ulNW4FRDdhokVgMJqzjoieelBlg9fCA5sf1j44pTXBKvJVVPjCaIH96ngm4sAelXwRprwacIn6F_SPzi194N7kT3bxmOp7TNElyGRkAffA9o_TN7TzslL4Q7C8hcRz04iTFF9idhcGr1Mf7e6de-2EOMaftGaCThdTCILxBh2OWaGELyfkGd77p4y4onlNpAt6-Vmz_V20Aw0ljNv2IQy8W0Ib_Rpoo5xkdInvBr8kwAGPNKqsMlX7EW-GN8K41IdEMMMtF5q0_F_J25PZirBS2AtbS_zApWnesGVh3qoVZ06ZmLOVxSsNAngjB8qeNp-gdTvWqH7TMiHy9qWlkfoRpkxxI1Mkdsv4LBEmICo3hgVfux25BCm1Muf7PcAO14kKpuBaORdybeX97AKEkWaD7I26L52j9I8_8P5cOVzQHf5jC0u8Xw6zikLenhM2-GrOa3vchcByTA13dl9u1dnooY4uyFUTSPD3aBquaSk5rqFfHV5SKVfaH4BCPlNOiXRZXQGGzxAE3beAyNDzBYH53DLY9tNPjtNp3Bbvc455irqVsh6zedAMyC51Pkh9WeNk0f5Rn0PbWBz1qHTLQALpQfD2pAekD0fuUuKgoIROeypoeNS0YB7yUleH86f22DeSepprsBkXQojaqoxky0QaanRqXaJBvfkIaKjvLm0DCRSHg1N1XoJgoMuoTthcLGH5oGjAeoT7JHL0xVOxoDhNa1DP3_tnsSnmPuTahbHnzum_Dlu7nOahs8Vk1M2w46MWBnaQ0fEF7F-F7yx_26XsltevNx-dW0rKoi4MY-2v0WfDiQIfY-U5HZff-h9sveAtAcqKC4hTpDZjUTmnTVDI4pQ72vDXAKS4ye-hgnNQLzjCuj4ZrMoGnxY8f9aq0OB9r144h6VNZXdR5prV7XWMjH0jC7gj0jaK4rPjzqjmTd8T1LOJFHwDuPZF9ryAdNm3FUS14aCw8xKprAKGanC7kN_mvEdB2cEAPxofTwOnEFsa26OGCLzQbhkeBK-PBkyaNGrXxXpCqMZYyVQE7kyuH93WZOJwYsslUuCl03JxacmIRylL7hOTAZnJhIeLLt4xl7VPoYSUnwzLdzc1zRpPYJz_7-F-e5Oq2HPINoYOyzss2temB9AY9ilzxEi0vjz_HhYX-vJAWOFIRArIKvUkNYfcPvRtEWLdnPY0ezbezZQDuSwlMrrXtR1h_MUV9lFgIfzOc5DeRxQsa_DzD81kVsf2X0it1ITszHhR222iDGVkBhSqx8HgkDYSwWj0XwwyddKsWu3Z89ogMA3uOWUV__EbssGeIzQFwrO8AZBq1_f0bACCnQxQMmvj4SpLco1toaui8NXkuQ6JExU9gwmX6drc2VLHPodnfQzX2nfzpUnRDzqVuKEnLHAwQQc18gL1crt3WMHzdlXIKq58ym_JCIMCKrU476PxJd6sioDlzFfxjLFpPpkdr4fnfFDmFbpUIcUrM83Z4jsLUB2e8ip82l-Wks1pOzyRvySWPayMVpYKgG9KcLlUxORP21_K-usWjHXXmScXmuFkyANibB5IDGwAyIFgXyihJc5arVi04R4YCJvIWSZIRJQ_gKRFftEr7CToqGt642WAe8mgHdG1oG3JSZMBa1cZB9z0XKxBqEBfgkDXH7-AqS8-v65M_tIymWPQoYel3_8thBMlpRx6GvLakxZu_ACepePPSWdZiEUHIXNtbNf96JPy0GqOF5v4wwIYHGIWSto5wmoXVWEqMuey-mH3DdUi70dUmruV2dHXhTRkM",
    "encodedPassword": "UGFwaUxhem8yMDAwIQ=="
}

response = requests.post(url, headers=headers, json=payload)

# Print the response
print("Response Headers:", response.headers)
print("Response Content:", response.content)

try:
    response_json = response.json()
    print(response_json)
except ValueError as e:
    print("Failed to parse response as JSON:", e)
    print("Raw response content:", response.content)
