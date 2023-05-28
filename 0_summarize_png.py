# %%
from PIL import Image, ImageStat, ImageFile
import datetime
import pandas as pd
import os

ImageFile.LOAD_TRUNCATED_IMAGES = True


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
