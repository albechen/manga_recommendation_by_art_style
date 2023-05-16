# %%
import os
import pandas as pd


# %%
def read_all_csv_in_folder(path, output_folder, file_name):
    csv_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".csv")]
    final_df = pd.DataFrame()

    for csv in csv_paths:
        temp_df = pd.read_csv(csv)
        final_df = pd.concat([final_df, temp_df], ignore_index=True)

    output_path = output_folder + file_name + ".csv"
    final_df = final_df.sort_values("rank")
    final_df.to_csv(output_path, index=False)


# %%
############### 2_mal_dl_info ###############
path = "data/raw/mal_data_tables/"
output_folder = "data/raw/"
file_name = "mal_data"
read_all_csv_in_folder(path, output_folder, file_name)


# %%
############### 3_mal_to_mdex_link ###############
path = "data/raw/mdex_link_tables/"
output_folder = "data/raw/"
file_name = "mdex_link"
read_all_csv_in_folder(path, output_folder, file_name)


def update_mdex_link(row):
    if row["link_method"] == "mdex":
        full_link = "https://mangadex.org" + row["mdex_link"]
    elif row["link_method"] == "google":
        full_link = row["mdex_link"]
    else:
        return None

    return full_link.split("?")[0]


mdex_links_df = pd.read_csv("data/raw/mdex_link.csv")
mdex_links_df["updated_mdex_link"] = mdex_links_df.apply(
    lambda row: update_mdex_link(row), axis=1
)
mdex_links_df.to_csv("data/raw/mdex_link.csv", index=False)


# %%
############### 4_mdex_dl_info ###############
path = "data/raw/mdex_data_tables/"
output_folder = "data/raw/"
file_name = "mdex_data"
read_all_csv_in_folder(path, output_folder, file_name)


def get_mal_id_from_mal_link(row):
    mal_link = str(row["mdex_mal_link"])
    prefix = "https://myanimelist.net/manga/"
    if mal_link != "nan":
        if mal_link.startswith(prefix):
            mal_link = mal_link[len(prefix) :]
        mal_id = int(mal_link.split("/")[0])
        return mal_id
    return None


mdex_data_df = pd.read_csv("data/raw/mdex_data.csv")
mdex_data_df["mdex_mal_id"] = mdex_data_df.apply(
    lambda row: get_mal_id_from_mal_link(row), axis=1
)
mdex_data_df.to_csv("data/raw/mdex_data.csv", index=False)


# %%
############### 5_mal_user_table_dl ###############
path = "data/raw/mal_user_list_tables/"
output_folder = "data/raw/"
file_name = "mal_user_list"
read_all_csv_in_folder(path, output_folder, file_name)

mal_user_list_df = pd.read_csv("data/raw/mal_user_list.csv")
dedup_mal_users = list(set(mal_user_list_df["Member"].to_list()))
unique_mal_users = pd.DataFrame(dedup_mal_users, columns=["mal_username"])
unique_mal_users = unique_mal_users.sort_values(by=["mal_username"])
unique_mal_users = unique_mal_users.reset_index(drop=True)
unique_mal_users["user_index"] = unique_mal_users.index
unique_mal_users.to_csv("data/raw/unique_mal_users.csv", index=False)


# %%
############### 7_mal_user_read_list ###############
# path = "data/raw/mal_user_manga_list/"
# output_folder = "data/raw/"
# file_name = "mal_user_manga_list"
# read_all_csv_in_folder(path, output_folder, file_name)
