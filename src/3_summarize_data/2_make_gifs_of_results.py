# %%
from PIL import Image
import os


# %%
def join_images_side_by_side(image_path1, image_path2, output_path):
    image1 = Image.open(image_path1)
    image2 = Image.open(image_path2)

    width1, height1 = image1.size
    width2, height2 = image2.size

    total_width = width1 + width2
    max_height = max(height1, height2)

    new_image = Image.new("RGB", (total_width, max_height))
    new_image.paste(image1, (0, 0))
    new_image.paste(image2, (width1, 0))
    new_image.save(output_path)


# %%
def find_png_files_with_prefix(folder_path, prefix):
    png_files = []
    for filename in os.listdir(folder_path):
        if filename.lower().startswith(prefix.lower()) and filename.lower().endswith(
            ".png"
        ):
            png_files.append(os.path.join(folder_path, filename))

    return png_files


def get_png_files_names_with_full(folder_path, prefix):
    full_png_names = []
    for filename in os.listdir(folder_path):
        if filename.lower().startswith(prefix.lower()) and filename.lower().endswith(
            ".png"
        ):
            full_file_name = "full_" + filename
            full_png_names.append(os.path.join(folder_path, full_file_name))

    return full_png_names


def save_gif(dataset, hue, path):
    path = path + "/{0}/{1}".format(dataset, hue)
    prefix = "{0}_{1}_".format(dataset, hue)

    full_png_names = get_png_files_names_with_full(path, prefix)
    image_list = find_png_files_with_prefix(path, prefix)

    for single_img, full_img in zip(image_list, full_png_names):
        summary_img = path + "/" + prefix + ".png"
        join_images_side_by_side(summary_img, single_img, full_img)

    f_image_list = find_png_files_with_prefix(path, "full_" + prefix)

    images = []
    for f_image_file in f_image_list:
        img = Image.open(f_image_file)
        images.append(img)

    images.append(images.pop(0))
    images.append(images[-1])

    output_path = path + "/" + prefix + ".gif"
    images[0].save(
        output_path,
        save_all=True,
        append_images=images[1:],
        optimize=False,
        duration=500,
        loop=0,
    )


# %%
path = "data/images/results"
dataset_list = ["image_pca", "doc2vec", "tag_svd"]
hue_list = ["starting_decade", "mal_demographic", "mean_score"]

for dataset in dataset_list:
    for hue in hue_list:
        save_gif(dataset, hue, path)
# %%

# %%
