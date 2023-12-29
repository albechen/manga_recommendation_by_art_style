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
def get_random_pic_list_from_rank(rank_num):
    path = "data/images/manga/"
    rank_str = str(rank_num).zfill(5)
    rank_path = path + rank_str

    cover_path = "data/images/covers/" + rank_str
    cover_pic = os.listdir(cover_path)[0]
    cover_path = "/".join([cover_path, cover_pic])

    pic_list = os.listdir(rank_path)
    ran_pic_list = random.sample(pic_list, 5)
    ran_pic_list = [rank_path + "/" + pic for pic in ran_pic_list]
    ran_pic_list = [cover_path] + ran_pic_list
    return ran_pic_list


def merge_images_horizontal(pic_list):
    imgs = [Image.open(i).convert("RGB") for i in pic_list]
    min_shape = sorted([(np.sum(i.size), i.size) for i in imgs])[0][1]
    img_array = np.hstack([i.resize(min_shape) for i in imgs])
    imgs_comb = Image.fromarray(img_array)
    return imgs_comb


# %%
# path = "data/images/covers"
# for rank in os.listdir(path)[1198:]:
#     ran_imgs = get_random_pic_list_from_rank(rank)
#     h_img = merge_images_horizontal(ran_imgs)
#     h_img.save("data/images/summary/{}.jpg".format(rank), "JPEG")


# %%
rank = "9843"
rank = str(rank).zfill(5)
ran_imgs = get_random_pic_list_from_rank(rank)
h_img = merge_images_horizontal(ran_imgs)
h_img.save("data/images/summary/{}.jpg".format(rank), "JPEG")


# %%
def scale_image(image, target_width):
    # Calculate the scaling factor to achieve the target width
    scaling_factor = target_width / float(image.size[0])
    # Calculate the new height based on the scaling factor
    target_height = int(float(image.size[1]) * float(scaling_factor))
    # Resize the image
    resized_image = image.resize((target_width, target_height), Image.LANCZOS)
    return resized_image


path = "data/images/summary"
for rank in os.listdir(path):
    img = Image.open(path + "/" + rank)
    resized_image = scale_image(img, 1200)
    resized_image.save("data/images/summary_2/{}".format(rank), "JPEG")

# %%
