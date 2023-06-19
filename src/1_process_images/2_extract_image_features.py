# %%
import torch
import torchvision.models as models
import torchvision.transforms as T
from PIL import Image, ImageFile
import datetime
import os
import pandas as pd

ImageFile.LOAD_TRUNCATED_IMAGES = True


# %%
def transform_image_to_five_crops(image):
    five_crop_T = [
        T.Grayscale(num_output_channels=3),
        T.Resize(224 * 2),
        T.FiveCrop(224),
    ]
    five_crop = T.Compose(five_crop_T)

    five_imgs = five_crop(image)
    return five_imgs


def extract_features_from_img(model, cropped_img, mean, std):
    normarlize_T = [
        T.ToTensor(),
        T.Normalize(mean, std),
    ]
    normalize = T.Compose(normarlize_T)
    tensor_img = normalize(cropped_img)
    input_batch = tensor_img.unsqueeze(0)

    if torch.cuda.is_available():
        input_batch = input_batch.to("cuda")
        model.to("cuda")

    with torch.no_grad():
        output = model(input_batch)

    feature_vector = torch.flatten(output.cpu(), start_dim=1).numpy()

    return feature_vector


def features_from_five_cropped(cropped_imgs, model, mean, std):
    feature_vectors = [
        extract_features_from_img(model, cropped_img, mean, std)
        for cropped_img in cropped_imgs
    ]
    full_features = []
    for feature_vector in feature_vectors:
        full_features.extend(feature_vector.flatten())
    return full_features


# image = Image.open("data/images/test_manga//00007/00007_1_1_01.jpg")
# cropped_imgs = transform_image_to_five_crops(image)
# feature_vector = features_from_five_cropped(cropped_imgs, manga_mean, manga_std)


# %%
def download_features_based_on_paths(
    pic_path_list,
    rank_list,
    pic_name_list,
    model,
    mean,
    std,
    model_name,
    norm_name,
    start,
    end,
):
    pic_path_list_s = pic_path_list[start:end]
    rank_list_s = rank_list[start:end]
    pic_name_list_s = pic_name_list[start:end]

    len_subset = len(pic_path_list_s)
    pic_vectors = [0] * len_subset

    for n in range(len_subset):
        pic_path = pic_path_list_s[n]
        rank = rank_list_s[n]
        pic_name = pic_name_list_s[n]

        image = Image.open(pic_path)
        cropped_imgs = transform_image_to_five_crops(image)
        feature_vector = features_from_five_cropped(cropped_imgs, model, mean, std)

        pic_vector = [pic_path, rank, pic_name]
        pic_vector.extend(feature_vector)

        pic_vectors[n] = pic_vector

    column_names = ["pic_path", "rank", "pic_name"]
    for n in range(len(pic_vectors[0]) - 3):
        column_names.append("{}_{}_{}".format(model_name, norm_name, n))

    feature_vector = pd.DataFrame(pic_vectors, columns=column_names)

    os.makedirs("data/raw/features_{}_{}".format(model_name, norm_name), exist_ok=True)

    feature_vector.to_csv(
        "data/raw/features_{0}_{1}/features_{0}_{1}_{2}_{3}.csv".format(
            model_name, norm_name, start, end
        ),
        index=False,
    )


def get_pic_path_list(path):
    pic_path_list = []
    pic_name_list = []
    rank_list = []
    for rank in os.listdir(path):
        rank_path = "/".join([path, rank])
        pic_list = os.listdir(rank_path)
        for pic in pic_list:
            pic_path = "/".join([rank_path, pic])
            pic_path_list.append(pic_path)
            rank_list.append(rank)
            pic_name_list.append(pic)
    return pic_path_list, rank_list, pic_name_list


def get_time_diff(start_time, count, total_pic):
    total_seconds = int((datetime.datetime.now() - start_time).total_seconds())
    time_formatted = str(datetime.timedelta(seconds=total_seconds))

    pct_comp = round(count / total_pic * 100)

    est_total_time = int(total_pic / count * total_seconds)
    est_total_time_formated = str(datetime.timedelta(seconds=est_total_time))

    est_time_left = est_total_time - total_seconds
    est_time_left_formated = str(datetime.timedelta(seconds=est_time_left))

    print(
        "%:",
        pct_comp,
        ", Count:",
        count,
        ", Time Elaspsed:",
        time_formatted,
        ", Est. Total Time:",
        est_total_time_formated,
        ", Est. Time Left:",
        est_time_left_formated,
    )


# %%
def download_all(path, model, model_name, norm_name, mean, std, start_n):
    pic_path_list, rank_list, pic_name_list = get_pic_path_list(path)

    start_time = datetime.datetime.now()
    end_n = len(pic_path_list)
    num_pics = end_n - start_n
    inc_size = 10000

    while start_n < end_n:
        download_features_based_on_paths(
            pic_path_list,
            rank_list,
            pic_name_list,
            model,
            mean,
            std,
            model_name,
            norm_name,
            start_n,
            start_n + inc_size,
        )

        start_n += inc_size
        get_time_diff(start_time, start_n, num_pics)


# %%
manga_mean = [0.76752] * 3  # 195.7174731808421
manga_std = [0.356] * 3  # 90.7795438947151

standard_mean = [0.485, 0.456, 0.406]
standard_std = [0.229, 0.224, 0.225]

# %%
path = "data/images/manga"

model = models.convnext_large(weights="DEFAULT")
model = torch.nn.Sequential(*list(model.children())[:-1])
model.eval()

# %%
mean = manga_mean
std = manga_std
model_name = "CVN"
norm_name = "C"
start_n = 0

download_all(path, model, model_name, norm_name, mean, std, start_n)

# %%
mean = standard_mean
std = standard_std
model_name = "CVN"
norm_name = "S"
start_n = 0

download_all(path, model, model_name, norm_name, mean, std, start_n)

# %%
path = "data/images/manga"

model = models.alexnet(weights="DEFAULT")
model = torch.nn.Sequential(*list(model.children())[:-1])
model.eval()

# %%

mean = manga_mean
std = manga_std
model_name = "ALX"
norm_name = "C"
start_n = 0

download_all(path, model, model_name, norm_name, mean, std, start_n)

# %%

mean = standard_mean
std = standard_std
model_name = "ALX"
norm_name = "S"
start_n = 0

download_all(path, model, model_name, norm_name, mean, std, start_n)

# %%
import os
import pandas as pd


# %%
def read_all_csv_in_folder(path, output_folder, file_name):
    csv_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".csv")]
    output_path = output_folder + file_name + ".csv"

    CHUNK_SIZE = 50000

    first_one = True
    for csv_file_name in csv_paths:
        print(csv_file_name)
        if not first_one:
            skip_row = [0]
        else:
            skip_row = []

        chunk_container = pd.read_csv(
            csv_file_name, chunksize=CHUNK_SIZE, skiprows=skip_row
        )
        for chunk in chunk_container:
            chunk.to_csv(output_path, mode="a", index=False)
        first_one = False


# %%
path = "data/raw/features_ALX_C/"
output_folder = "data/raw/"
file_name = "features_ALX_C"
read_all_csv_in_folder(path, output_folder, file_name)
# %%

path = "data/raw/features_ALX_S/"
output_folder = "data/raw/"
file_name = "features_ALX_S"
read_all_csv_in_folder(path, output_folder, file_name)

path = "data/raw/features_CVN_C/"
output_folder = "data/raw/"
file_name = "features_ALX_C"
read_all_csv_in_folder(path, output_folder, file_name)

path = "data/raw/features_CVN_S/"
output_folder = "data/raw/"
file_name = "features_ALX_C"
read_all_csv_in_folder(path, output_folder, file_name)
# %%
