# %%
import pandas as pd
import re
import numpy as np

pd.set_option("display.max_columns", None)

# %%
############################################
# MAL DATA -- CLEAN DUPLICATE COLS
############################################


def comb_two_lists(list_a, list_b):
    if pd.isna(list_a):
        list_a = ""
    if pd.isna(list_b):
        list_b = ""
    return list_a + list_b


def get_single_phrase(string):
    pattern = r"(.+?)\s+\1"
    matches = re.findall(pattern, string)

    if len(matches) == 1:
        return matches[0]
    else:
        return string


def clean_repeated_list(raw_list):
    if pd.notna(raw_list):
        split_list = raw_list.split(", ")
        clean_list = [get_single_phrase(n) for n in split_list if n != ""]
        clean_list = list(set(clean_list))
        return clean_list
    return []


def combine_two_same_columns(df, col_a, col_b):
    list_a = df[col_a].to_list()
    list_b = df[col_b].to_list()

    list_ab = [comb_two_lists(a, b) for a, b in zip(list_a, list_b)]
    clean_col = [clean_repeated_list(n) for n in list_ab]
    return clean_col


def clean_all_duplicate_columns(df, comb_dict):
    for comb in comb_dict:
        col_a = comb[0]
        col_b = comb[1]
        clean_col = combine_two_same_columns(df, col_a, col_b)
        df[col_a] = clean_col
        df = df.drop(col_b, axis=1)
    return df


############################################
# MAL DATA -- CLEAN PUBLISHED
############################################


def search_year_in_str(string):
    match = re.search(r"\d{4}", string)
    if match:
        return match.group()
    return np.nan


def extract_published_years(publish_str):
    split_list = publish_str.split(" to ")
    years = [search_year_in_str(n) for n in split_list]
    if len(years) == 1:
        return [years[0], np.nan]
    if len(years) == 2:
        return [years[0], years[1]]
    return [np.nan, np.nan]


def extract_start_end_published_years(df):
    publish_list = df["Published"].to_list()
    publish_list = [extract_published_years(n) for n in publish_list]
    publish_df = pd.DataFrame(publish_list, columns=["start_year", "end_year"])
    df = pd.concat([df, publish_df], axis=1)
    df = df.drop("Published", axis=1)
    return df


############################################
# MAL DATA -- CLEAN INT NUMBERS
############################################
col_to_int = [
    "Members",
    "Favorites",
    "Reading",
    "Completed",
    "On-Hold",
    "Dropped",
    "Plan to Read",
    "Total",
]


def convert_comma_num_to_int(df, col_to_int):
    clean_df = df.copy()
    for col in col_to_int:
        clean_df[col] = clean_df[col].str.replace(",", "").astype(int)
    return clean_df


############################################
# MAL DATA -- CLEAN volumes and chapters
############################################
def clean_vol_and_chp(df):
    clean_df = df.copy()
    clean_df["Volumes"] = clean_df["Volumes"].replace("Unknown", np.nan)
    clean_df["Chapters"] = clean_df["Chapters"].replace("Unknown", np.nan)
    return clean_df


############################################
# MAL DATA -- GET TOTAL NUMBER SCORES
############################################
def get_total_scores(df):
    clean_df = df.copy()
    mal_score_columns = clean_df.filter(like="score")
    clean_df["score_total"] = mal_score_columns.sum(axis=1)
    clean_df = clean_df[clean_df["score_total"] >= 10]
    clean_df = clean_df.drop(["score_total"], axis=1)
    return clean_df


############################################
# MAL DATA  -- FULL CLEAN METHOD
############################################

mal_data_col = {
    "rank": "rank",
    "start_year": "mal_start_year",
    "end_year": "mal_end_year",
    "Volumes": "mal_volumes",
    "Chapters": "mal_chapters",
    "Status": "mal_status",
    "Genre": "mal_genre",
    "Theme": "mal_theme",
    "Demographic": "mal_demographic",
    "Members": "mal_members",
    "Favorites": "mal_favorites",
    "Reading": "mal_reading",
    "Completed": "mal_completed",
    "On-Hold": "mal_completed",
    "Dropped": "mal_dropped",
    "Plan to Read": "mal_planned",
    "Total": "mal_total",
    "score_10": "mal_score_100",
    "score_9": "mal_score_90",
    "score_8": "mal_score_80",
    "score_7": "mal_score_70",
    "score_6": "mal_score_60",
    "score_5": "mal_score_50",
    "score_4": "mal_score_40",
    "score_3": "mal_score_30",
    "score_2": "mal_score_20",
    "score_1": "mal_score_10",
}

mal_data_comb_dict = [
    ["Demographic", "Demographics"],
    ["Theme", "Themes"],
    ["Genre", "Genres"],
]


def clean_mal_data_df(df, mal_data_comb_dict, mal_data_col):
    clean_df = clean_all_duplicate_columns(df, mal_data_comb_dict)
    clean_df = extract_start_end_published_years(clean_df)
    clean_df = convert_comma_num_to_int(clean_df, col_to_int)
    clean_df = clean_vol_and_chp(clean_df)
    clean_df = get_total_scores(clean_df)
    clean_df = clean_df[list(mal_data_col)].rename(columns=mal_data_col)
    clean_df["mal_data"] = 1
    return clean_df


# %%
############################################
# MDEX DATA  -- FULL CLEAN METHOD
############################################
mdex_data_col = ["rank", "mdex_genre", "mdex_description"]


def clean_mdex_data_df(df_top, df_mdex, mdex_data_col):
    clean_mdex_data = df_top[["rank", "mal_id"]].merge(df_mdex, on="rank", how="left")
    clean_mdex_data["match_mal_id"] = (
        clean_mdex_data["mal_id"] == clean_mdex_data["mdex_mal_id"]
    )
    clean_mdex_data = clean_mdex_data.loc[clean_mdex_data["match_mal_id"] == True]
    clean_mdex_data = clean_mdex_data[mdex_data_col]
    clean_mdex_data["mdex_data"] = 1
    return clean_mdex_data


############################################
# ANI DATA  -- FULL CLEAN METHOD & GET TOTAL NUMBER SCORES
############################################
def clean_ani_data_df(df):
    clean_df = df.copy()
    ani_score_columns = clean_df.filter(like="ani_score")

    clean_df["score_total"] = ani_score_columns.sum(axis=1)
    clean_df = clean_df[clean_df["score_total"] >= 10]

    clean_df = clean_df.drop(["mal_id", "ani_id", "score_total"], axis=1)
    clean_df["ani_data"] = 1

    return clean_df


# %%
mal_top_manga = pd.read_csv("data/raw/mal_top_manga.csv")

mal_data = pd.read_csv("data/raw/mal_data.csv")
mdex_data = pd.read_csv("data/raw/mdex_data.csv")
ani_data = pd.read_csv("data/raw/ani_data.csv")

# %%
# clean_mdex_data = clean_mdex_data_df(mal_top_manga, mdex_data, mdex_data_col)
cleaned_mal_data = clean_mal_data_df(mal_data, mal_data_comb_dict, mal_data_col)
clean_ani_data = clean_ani_data_df(ani_data)

# %%
main_df = mal_top_manga[["rank", "title"]].copy()
main_df = main_df.rename(columns={"title": "mal_title"})
main_df = main_df.merge(cleaned_mal_data, on="rank", how="left")
main_df = main_df.merge(clean_ani_data, on="rank", how="left")
main_df = main_df.loc[(main_df["ani_data"] == 1) & (main_df["mal_data"] == 1), :]

main_df.head()

# %%
main_df.to_csv("data/interim/manga_site_features_combined.csv", index=False)
# %%
