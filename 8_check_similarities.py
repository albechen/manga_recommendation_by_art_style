# %%
import pandas as pd
import matplotlib.pyplot as plt
import os
from PIL import Image
import random
import numpy as np
from IPython.display import display

# %%
df = pd.read_csv("data/processed/image_feature_similarity.csv")


# %%
def get_random_pic_list_from_rank(rank_num):
    path = "data/images/manga/"
    rank_str = str(rank_num).zfill(5)
    rank_path = path + rank_str

    pic_list = os.listdir(rank_path)
    ran_pic_list = random.sample(pic_list, 5)
    ran_pic_list = [rank_path + "/" + pic for pic in ran_pic_list]
    return ran_pic_list


def merge_images_horizontal(pic_list):
    imgs = [Image.open(i) for i in pic_list]
    min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
    img_array = np.hstack([i.resize(min_shape) for i in imgs])
    imgs_comb = Image.fromarray(img_array)
    display(imgs_comb)
    return img_array


# def merge_images_vertically(pic_list):
#     imgs = pic_list
#     min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
#     img_array = np.vstack([i.resize(min_shape) for i in imgs])
#     return img_array


# %%
rank_num = "10802"
top_n = 5
similarities = df[["rank", rank_num]].sort_values(rank_num, ascending=False)
top_similar = similarities.head(top_n)
top_ranks = top_similar["rank"].to_list()

pic_list = []
for rank in [rank_num] + top_ranks:
    print(rank)
    ran_imgs = get_random_pic_list_from_rank(rank)
    h_img = merge_images_horizontal(ran_imgs)
    pic_list.append(h_img)

# full_img = merge_images_vertically(pic_list)
# imgs_comb = Image.fromarray(full_img)
# display(imgs_comb)

# %%


# %%
# data_array = df.drop(["rank"], axis=1).values
# data_list = data_array.flatten().tolist()
# random_items = random.sample(data_list, 1000000)

# plt.hist(random_items)
# plt.xlabel("Values")
# plt.ylabel("Frequency")
# plt.title("Histogram")
# plt.show()
