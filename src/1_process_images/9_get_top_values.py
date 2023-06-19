# %%
import pandas as pd
import matplotlib.pyplot as plt
import os
from PIL import Image, ImageFile
import random
import numpy as np
from IPython.display import display

ImageFile.LOAD_TRUNCATED_IMAGES = True

# %%
df = pd.read_csv("data/processed/image_feature_similarity.csv")


# %%
def merge_images_horizontal(pic_list):
    imgs = [Image.open(i).convert("RGB") for i in pic_list]
    min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
    img_array = np.hstack([i.resize(min_shape) for i in imgs])
    imgs_comb = Image.fromarray(img_array)
    # display(imgs_comb)
    return imgs_comb


# def merge_images_vertically(pic_list):
#     imgs = pic_list
#     min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
#     img_array = np.vstack([i.resize(min_shape) for i in imgs])
#     return img_array

# %%
rank_num = "9843"
top_n = 5
similarities = df[["rank", rank_num]].sort_values(rank_num, ascending=False)
top_similar = similarities.head(top_n)
top_ranks = top_similar["rank"].to_list()

for rank in [rank_num] + top_ranks:
    print(rank)
    rank_str = str(rank).zfill(5)
    summary_img = Image.open("data/images/summary/{}.jpg".format(rank_str))
    display(summary_img)

# full_img = merge_images_vertically(pic_list)
# imgs_comb = Image.fromarray(full_img)
# display(imgs_comb)

# %%
sample_list = random.sample(similarities["rank"].to_list(), 1000)
for rank in sample_list:
    print(rank)
    rank_str = str(rank).zfill(5)
    summary_img = Image.open("data/images/summary/{}.jpg".format(rank_str))
    display(summary_img)

# %%
# data_array = df.drop(["rank"], axis=1).values
# data_list = data_array.flatten().tolist()
# random_items = random.sample(data_list, 1000000)

# plt.hist(random_items)
# plt.xlabel("Values")
# plt.ylabel("Frequency")
# plt.title("Histogram")
# plt.show()
