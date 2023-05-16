# %%
import os
import re
import shutil
import json


# %%
def get_vol_ch_folder_name(folder_name):
    folder_adj = re.sub(r"\[.*?\]", "", folder_name)
    folder_adj = folder_adj.replace(" ", "")

    vol_id = "Vol."
    ch_id = "Ch."
    vol_idx = folder_adj.find(vol_id)
    ch_idx = folder_adj.find(ch_id)

    if vol_idx != -1 and ch_idx != -1:
        vol_num = folder_adj[vol_idx + len(vol_id) : ch_idx]
        ch_num = folder_adj[ch_idx + len(ch_id) :]
        if vol_num == "0" or "." in ch_num:
            vol_num = "99"
    else:
        vol_num = "99"
        ch_num = "99"

    return [vol_num, ch_num, folder_name]


def sort_folder_order(folder_list):
    to_remove = ["download.db", "cover.jpg"]
    rmv_list = [x for x in folder_list if x not in to_remove]
    vol_chp_folders = [get_vol_ch_folder_name(n) for n in rmv_list]
    vol_chp_folders.sort()
    return vol_chp_folders


# %%
def get_images_to_rename_and_move(folder_list, rank, manga_dict):
    vol_chp_folders = sort_folder_order(folder_list)

    rank_path = manga_dict["rank_path"]
    title_path = manga_dict["title_path"]

    og_img_list = []
    new_img_list = []

    for folder in vol_chp_folders:
        folder_vol = folder[0]
        folder_ch = folder[1]
        folder_path = folder[2]

        folder_names_list = "/".join([title_path, folder_path])
        og_img_names = os.listdir(folder_names_list)
        og_img_names = og_img_names[:25]  # only carry over first 25 images

        og_img_paths = ["/".join([folder_names_list, pg]) for pg in og_img_names]
        og_img_list.extend(og_img_paths)

        new_img_names = [
            "_".join([rank, folder_vol, folder_ch, x]) for x in og_img_names
        ]
        new_img_paths = ["/".join([rank_path, pg]) for pg in new_img_names]
        new_img_list.extend(new_img_paths)

    return og_img_list, new_img_list


# %%
path = "data/images/manga"
rank_list = [rank for rank in os.listdir(path)]
all_dict = []

# idx = rank_list.index("08519")
# idx
# rank_list[idx : idx + 1]
# %%
manga_img_list = []
for rank in rank_list:
    try:
        rank_path = "/".join([path, rank])
        title_path = "/".join([rank_path, os.listdir(rank_path)[0]])
        og_cover_path = "/".join([title_path, "cover.jpg"])
        new_cover_path = "data/images/covers/{}.jpg".format(rank)

        manga_dict = {
            "rank": rank,
            "rank_path": rank_path,
            "title_path": title_path,
            "og_cover_path": og_cover_path,
            "new_cover_path": new_cover_path,
        }

        folder_list = os.listdir(title_path)
        if len(folder_list) <= 2:
            manga_dict["has_chp"] = False
        else:
            manga_dict["has_chp"] = True
            og_img_list, new_img_list = get_images_to_rename_and_move(
                folder_list, rank, manga_dict
            )
            manga_dict["og_img_list"] = og_img_list
            manga_dict["new_img_list"] = new_img_list
        manga_img_list.append(manga_dict)
    except:
        print(rank)

# %%

for manga_dict in manga_img_list[8795:]:
    try:
        if manga_dict["has_chp"] == False:
            rank_path = manga_dict["rank_path"]
            shutil.rmtree(rank_path)

        else:
            og_img_list = manga_dict["og_img_list"]
            new_img_list = manga_dict["new_img_list"]

            og_cover_path = manga_dict["og_cover_path"]
            new_cover_path = manga_dict["new_cover_path"]

            og_list = og_img_list + [og_cover_path]
            new_list = new_img_list + [new_cover_path]

            for og, new in zip(og_list, new_list):
                shutil.move(og, new)

            title_path = manga_dict["title_path"]
            shutil.rmtree(title_path)
    except:
        print(manga_dict["rank"])

# %%
# 10326
