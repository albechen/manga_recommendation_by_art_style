# %%
import os
import pandas as pd
import datetime
import time
import re
import shutil

# %%
df = pd.read_csv("data/processed/image_feature_similarity.csv")

# %%
##############
# DOWNLOAD COVERS
##############
ranks = df.columns.to_list()
ranks.remove("rank")
ranks = [int(rank) for rank in ranks]

# %%
mdex = pd.read_csv("data/raw/mdex_link.csv")[["rank", "updated_mdex_link"]]
filtered_df = mdex[mdex["rank"].isin(ranks)]
filtered_df

mdex_links = filtered_df["updated_mdex_link"].to_list()
ranks = filtered_df["rank"].to_list()


# %%
start_time = datetime.datetime.now()
start_n = 0
end_n = len(ranks)
sleep_time = 2

for link, rank in zip(mdex_links[start_n:end_n], ranks[start_n:end_n]):
    total_seconds = (datetime.datetime.now() - start_time).total_seconds()
    time_formatted = str(datetime.timedelta(seconds=total_seconds))
    print(rank, time_formatted, link)

    path = '"data/images/covers/{:05d}"'.format(rank)
    mdex_cmd = 'mangadex-dl "cover:{}" --input-pos "*" --path "{}"'.format(link, path)
    os.system(mdex_cmd)

    time.sleep(sleep_time)


# %%
##############
# REORG COVERS
##############
# %%
def check_string(string, count):
    pattern = r"Volume (\d+) cover"
    match = re.search(pattern, string)
    if match:
        number = float(match.group(1))
        return number, count
    else:
        count = count + 1
        return count, count


string = "Volume 2 cover.jpg"

count = 0
number, count = check_string(string, count)
number, count

# %%
path = "data/images/covers"
for rank in os.listdir(path):
    rank_path = "/".join([path, rank])
    title_list = os.listdir(rank_path)

    for title in title_list:
        title_path = "/".join([rank_path, title])
        pic_list = os.listdir(title_path)
        pic_vol = []
        count = 90

        for pic in pic_list:
            pic_path = "/".join([title_path, pic])
            number, count = check_string(pic, count)
            pic_vol.append([number, pic_path])

        pic_vol.sort()
        first_cover_path = pic_vol[0][1]
        path_move_to = "/".join([rank_path, first_cover_path[-9:]])
        folder_to_delete = title_path

        try:
            shutil.move(first_cover_path, path_move_to)
            shutil.rmtree(folder_to_delete)
        except:
            print(rank, first_cover_path)

# %%
