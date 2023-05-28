# %%
import requests
import json
import pandas as pd
import datetime
import time

with open("data/tokens/token_ani.json") as f:
    token = json.load(f)

with open("data/tokens/secrets.json") as f:
    secret_json = json.load(f)

CLIENT_ID = secret_json["ani_CLIENT_ID"]
CLIENT_SECRET = secret_json["ani_CLIENT_SECRET"]
REDIRECT_URL = "https://httpbin.org/anything"
access_token = token["access_token"]


# %%
def get_tag_collection():
    query = """
    query testQuery{
        MediaTagCollection {
            id
            name
            description
            category
        }
    }
    """
    url = "https://graphql.anilist.co"
    response = requests.post(url, json={"query": query})
    tag_json = response.json()

    with open("data/raw/tag_collection.json", "w") as file:
        json.dump(tag_json, file, indent=4)

    return tag_json


tag_json = get_tag_collection()


# %%
def post_response_from_mal_id(mal_id):
    query = """
    query ($idMal: Int) {
        Media(idMal: $idMal, type: MANGA) {
            id
            idMal
            title {
            romaji
            english
            }
            meanScore
            averageScore
            genres
            description
            stats{
            scoreDistribution {
                score
                amount
            }
            statusDistribution {
                status
                amount
            }
            }
            tags{
            rank
            id
            }
        }
    }
    """
    variables = {"idMal": mal_id}
    url = "https://graphql.anilist.co"
    response = requests.post(url, json={"query": query, "variables": variables})

    return response


def convert_response_to_dict(response, rank):
    body = response.json()["data"]["Media"]
    ani_dict = {
        "rank": rank,
        "ani_id": body["id"],
        "mal_id": body["idMal"],
        "ani_meanScore": body["meanScore"],
        "ani_averageScore": body["averageScore"],
        "ani_genres": body["genres"],
        "ani_description": body["description"],
    }

    score_dist = body["stats"]["scoreDistribution"]
    for n in range(len(score_dist)):
        score_name = "ani_score_{}".format(score_dist[n]["score"])
        ani_dict[score_name] = score_dist[n]["amount"]

    status_dist = body["stats"]["statusDistribution"]
    for n in range(len(status_dist)):
        status_name = "ani_status_{}".format(status_dist[n]["status"])
        ani_dict[status_name] = status_dist[n]["amount"]

    tags = body["tags"]
    for n in range(len(tags)):
        status_name = "ani_tag_{}".format(tags[n]["id"])
        ani_dict[status_name] = tags[n]["rank"]

    return ani_dict


def download_anilist_manga_data(mal_id_list, rank_list, start, end):
    s_id = mal_id_list[start:end]
    s_rank = rank_list[start:end]
    manga_list = []

    error_count = 0

    for id, rank in zip(s_id, s_rank):
        time.sleep(1)
        response = post_response_from_mal_id(id)

        if response.status_code == 200:
            try:
                manga_dict = convert_response_to_dict(response, rank)
                manga_list.append(manga_dict)
                error_count = 0
                print(rank)
            except:
                print("FAIL - dict", id, rank, response.json())

        else:
            print("FAIL - ", response, id, rank, response.json())
            error_count += 1

        if error_count > 10:
            break

    manga_list_df = pd.DataFrame(manga_list)
    manga_list_df.to_csv(
        "data/raw/ani_data_tables/ani_data_{}_to_{}.csv".format(start, end),
        index=False,
    )

    return error_count


# %%
top_mal = pd.read_csv("data/raw/mal_top_manga.csv")
mal_id_list = top_mal["mal_id"].to_list()
rank_list = top_mal["rank"].to_list()

# %%
start_time = datetime.datetime.now()
prior_time = datetime.datetime.now()
start_n = 1200
end_n = len(rank_list)
inc_size = 100
error_count = 0

while start_n < end_n and error_count < 10:
    error_count = download_anilist_manga_data(
        mal_id_list, rank_list, start_n, start_n + inc_size
    )

    total_seconds = (datetime.datetime.now() - start_time).total_seconds()
    time_formatted = str(datetime.timedelta(seconds=total_seconds))

    total_seconds_since_prior = (datetime.datetime.now() - prior_time).total_seconds()
    time_formatted_prior = str(datetime.timedelta(seconds=total_seconds_since_prior))

    prior_time = datetime.datetime.now()

    print(start_n, time_formatted_prior, time_formatted)
    start_n += inc_size

# %%
