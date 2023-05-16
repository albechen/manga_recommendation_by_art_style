# %%
import requests
import json


with open("data/tokens/secrets.json") as f:
    secret_json = json.load(f)

CLIENT_ID = secret_json["ani_CLIENT_ID"]
CLIENT_SECRET = secret_json["ani_CLIENT_SECRET"]
REDIRECT_URL = "https://httpbin.org/anything"


# %%
def print_new_authorisation_url():
    global CLIENT_ID, REDIRECT_URL
    print(
        "https://anilist.co/api/v2/oauth/authorize?client_id={}&redirect_uri={}&response_type=code".format(
            CLIENT_ID, REDIRECT_URL
        )
    )


# %%
# 3. Once you've authorised your application, you will be redirected to the webpage you've
#    specified in the API panel. The URL will contain a parameter named "code" (the Authorisation
#    Code). You need to feed that code to the application.
def generate_new_token(authorisation_code: str) -> dict:
    global CLIENT_ID, CLIENT_SECRET

    url = "https://anilist.co/api/v2/oauth/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": authorisation_code,
        "redirect_uri": REDIRECT_URL,
        "grant_type": "authorization_code",
    }

    response = requests.post(url, data)
    response.raise_for_status()  # Check whether the request contains errors

    token = response.json()
    response.close()
    print("Token generated successfully!")

    with open("data/tokens/token_ani.json", "w") as file:
        json.dump(token, file, indent=4)
        print('Token saved in "token.json"')

    return token


# %%
print_new_authorisation_url()
# %%
authorisation_code = input("Copy-paste the Authorisation Code: ").strip()
# %%
token = generate_new_token(authorisation_code)
