# %%
import requests
import json
import pandas as pd
import datetime
import time
import random

with open("data/tokens/token_mal.json") as f:
    token = json.load(f)

with open("data/tokens/secrets.json") as f:
    secret_json = json.load(f)

access_token = token["access_token"]
CLIENT_ID = secret_json["mal_CLIENT_ID"]
CLIENT_SECRET = secret_json["mal_CLIENT_SECRET"]


# %%
def get_user_list(username, access_token):
    base_url = "https://api.myanimelist.net/v2/users/"
    fields = "/mangalist?fields=id,list_status&limit=1000&sort=list_score"
    url = base_url + username + fields

    response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"})
    status_code = response.status_code
    try:
        response_json = response.json()
    except:
        response_json = None
    response.close()
    return response_json, status_code


def extract_manga_from_response_json(username, user_idx, response_json):
    user_manga_list = []
    for manga_json in response_json["data"]:
        manga_dict = {
            "mal_username": username,
            "user_index": user_idx,
            "mal_id": manga_json["node"]["id"],
            "title": manga_json["node"]["title"],
            "status": manga_json["list_status"]["status"],
            "score": manga_json["list_status"]["score"],
        }
        user_manga_list.append(manga_dict)
    return user_manga_list


def download_mal_user_manga_list(user_list, user_ids, start, end):
    s_users = user_list[start:end]
    s_user_ids = user_ids[start:end]
    manga_list = []

    error_count = 0

    for username, user_idx in zip(s_users, s_user_ids):
        sleep_time = random.randint(3, 4) / 2
        time.sleep(sleep_time)
        response_json, status_code = get_user_list(username, access_token)

        if status_code == 200:
            try:
                user_manga_list = extract_manga_from_response_json(
                    username, user_idx, response_json
                )
                manga_list.extend(user_manga_list)
                error_count = 0
                print(user_idx)
            except:
                print("FAIL - dict", username, user_idx, response_json)

        if status_code in [400, 404, 401, 403]:
            print("FAIL - ", username, user_idx, status_code, response_json)
            error_count += 1

        if error_count > 10:
            break

    manga_list_df = pd.DataFrame(manga_list)
    manga_list_df.to_csv(
        "data/raw/mal_user_manga_list/mal_mangaList__{}_to_{}.csv".format(start, end),
        index=False,
    )

    return error_count


# %%
unique_users = pd.read_csv("data/raw/unique_mal_users.csv")
unique_user_list = unique_users["mal_username"].to_list()
user_index = unique_users["user_index"].to_list()

# %%
start_time = datetime.datetime.now()
prior_time = datetime.datetime.now()
start_n = 64500
end_n = len(user_index)
inc_size = 100
sleep_time = 15
error_count = 0

while start_n < end_n and error_count < 10:
    error_count = download_mal_user_manga_list(
        unique_user_list, user_index, start_n, start_n + inc_size
    )

    total_seconds = (datetime.datetime.now() - start_time).total_seconds()
    time_formatted = str(datetime.timedelta(seconds=total_seconds))

    total_seconds_since_prior = (datetime.datetime.now() - prior_time).total_seconds()
    time_formatted_prior = str(datetime.timedelta(seconds=total_seconds_since_prior))

    prior_time = datetime.datetime.now()

    print(start_n, time_formatted_prior, time_formatted)
    start_n += inc_size

    time.sleep(sleep_time)


# %%
# %%
# error_count = download_mal_user_manga_list(unique_user_list, user_index, 0, 3)
# username = "Matsun0"
# response_json, status_code = get_user_list(username, access_token)

# # %%
# extract_manga_from_response_json(username, response_json)
