# %%
from PIL import Image, ImageStat, ImageFile
import datetime
import pandas as pd
import os
import numpy as np

# ImageFile.LOAD_TRUNCATED_IMAGES = True


# %%=
def open_image(path):
    return Image.open(path)


def is_grayscale(image):
    im = image.convert("RGB")
    stat = ImageStat.Stat(im)
    if sum(stat.sum) / 3 == stat.sum[0]:
        return True
    else:
        return False


def pct_white_black_and_height_width(image):
    grayscale_image = image.convert("L")
    width, height = grayscale_image.size
    total_pixels = width * height
    greyscale_data = grayscale_image.getdata()

    white_pixels = sum(1 for pixel in greyscale_data if pixel > 240)
    pct_white = (white_pixels / total_pixels) * 100

    black_pixels = sum(1 for pixel in greyscale_data if pixel < 25)
    pct_black = (black_pixels / total_pixels) * 100

    return pct_white, pct_black, width, height


def get_image_data(pic_path, rank):
    image = open_image(pic_path)

    is_gray = is_grayscale(image)
    pct_white, pct_black, width, height = pct_white_black_and_height_width(image)

    pic_dict = {
        "rank": rank,
        "pic_path": pic_path,
        "is_grayscale": is_gray,
        "pct_white": pct_white,
        "pct_black": pct_black,
        "width": width,
        "height": height,
    }

    return pic_dict


def get_pic_path_list(path):
    pic_path_list = []
    rank_list = []
    for rank in os.listdir(path):
        rank_path = "/".join([path, rank])
        pic_list = os.listdir(rank_path)
        for pic in pic_list:
            pic_path = "/".join([rank_path, pic])
            pic_path_list.append(pic_path)
            rank_list.append(rank)
    return pic_path_list, rank_list


# %%
path = "data/images/manga"
pic_path_list, rank_list = get_pic_path_list(path)
total_pic = len(pic_path_list)
pic_summary = [0] * total_pic
total_pic

# %%
##############
# GET SUMMARY
##############
start_time = datetime.datetime.now()
prior_time = datetime.datetime.now()
count = 0

for n in range(total_pic):
    pic_path = pic_path_list[n]
    rank = rank_list[n]

    pic_dict = get_image_data(pic_path, rank)
    pic_summary[n] = pic_dict

    count += 1
    if count % 1000 == 0:
        total_seconds = (datetime.datetime.now() - start_time).total_seconds()
        time_formatted = str(datetime.timedelta(seconds=total_seconds))

        total_seconds_since_prior = (
            datetime.datetime.now() - prior_time
        ).total_seconds()
        time_formatted_prior = str(
            datetime.timedelta(seconds=total_seconds_since_prior)
        )

        prior_time = datetime.datetime.now()
        pct_comp = round(count / total_pic * 100)
        print(pct_comp, count, time_formatted_prior, time_formatted, rank)

# pic_summary = [get_image_data(x["pic_path"], x["rank"]) for x in pic_path_list]
# %%
pic_summary_csv = pd.DataFrame(pic_summary)
pic_summary_csv.to_csv("data/images/pic_summary.csv", index=False)


# %%
##############
# GET MEAN AND STD
##############
start_time = datetime.datetime.now()
prior_time = datetime.datetime.now()
count = 0

# Initialize variables for accumulating pixel values
pixel_sum = 0
pixel_squared_sum = 0
pixel_count = 0

import random

random_sample = random.sample(pic_path_list, k=10000)

img_paths = pic_path_list

for image_path in img_paths:
    image = Image.open(image_path)
    if image.mode != "L":
        image = image.convert("L")
        image.save(image_path)

    image_array = np.array(image).astype("uint64")

    # Accumulate the sum of pixel values and squared pixel values
    pixel_sum += np.sum(image_array, axis=(0, 1))
    pixel_squared_sum += np.sum(np.square(image_array, dtype="uint64"), axis=(0, 1))

    # Update the count of pixels
    pixel_count += image_array.shape[0] * image_array.shape[1]
    count += 1
    if count % 1000 == 0:
        total_seconds = (datetime.datetime.now() - start_time).total_seconds()
        time_formatted = str(datetime.timedelta(seconds=total_seconds))

        total_seconds_since_prior = (
            datetime.datetime.now() - prior_time
        ).total_seconds()
        time_formatted_prior = str(
            datetime.timedelta(seconds=total_seconds_since_prior)
        )

        prior_time = datetime.datetime.now()
        pct_comp = round(count / total_pic * 100)

        mean = pixel_sum / pixel_count
        std = np.sqrt(pixel_squared_sum / pixel_count - mean**2)
        print(mean, std, pct_comp, count, time_formatted_prior, time_formatted)

# Compute the mean and standard deviation
mean = pixel_sum / pixel_count
std = np.sqrt(pixel_squared_sum / pixel_count - mean**2)

# Print the computed mean and standard deviation
print("Mean:", mean)
print("Standard Deviation:", std)
print("count:", pixel_count)


# %%
##############
# GET SUMMARY
##############
import shutil

# Specify the directory containing the images
path = "data/images/manga"
for rank in os.listdir(path):
    print(rank)
    rank_path = "/".join([path, rank])
    pic_list = os.listdir(rank_path)
    for pic in pic_list:
        pic_path = "/".join([rank_path, pic])

        try:
            # Open the image using PIL
            with Image.open(pic_path) as image:
                # Check if the image is truncated
                image.load()
        except OSError as e:
            # The image is truncated, delete it
            shutil.move(pic_path, "data/images/deleted/{}".format(pic))
            print(f"Deleted {pic_path} - Truncated Image")

# %%
delete_folder = "data/images/deleted/"
deleted_list = os.listdir(delete_folder)
deleted_path_list = [delete_folder + img for img in deleted_list]
deleted_path_list
