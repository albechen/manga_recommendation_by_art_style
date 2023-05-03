# %%
import os
import pandas as pd

path = "data/key_tables/mdex_link_tables/"
mdex_csvs = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".csv")]

mdex_links = pd.DataFrame()
for file in mdex_csvs:
    temp_df = pd.read_csv(file)
    mdex_links = pd.concat([mdex_links, temp_df], ignore_index=True)

mdex_links


# %%
def mdex_logic(row):
    if row["link_method"] == "mdex":
        return "https://mangadex.org" + row["mdex_link"]
    if row["link_method"] == "google":
        return row["mdex_link"]
    else:
        return None


# apply the function to create the new column
mdex_links["updated_mdex_link"] = mdex_links.apply(lambda row: mdex_logic(row), axis=1)

# %%
mdex_link_list = mdex_links["updated_mdex_link"].to_list()
rank_list = mdex_links["rank"].to_list()

# "{:0>5}".format(num)


# %%

import os

link = '"https://mangadex.org/title/2f9ccb4f-9421-44c7-b9e4-89a62c6d10ea"'
path = '"data/images/test_1"'
os.system(
    'mangadex-dl {} --use-compressed-image --start-chapter 1 --end-chapter 1 --cover "512px" --delay-requests 2 --start-page 4 --end-page 8 --path "{}"'.format(
        link, path
    )
)

# %%
