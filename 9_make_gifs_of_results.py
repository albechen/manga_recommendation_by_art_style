# %%
from PIL import Image
import os


# %%
def find_png_files_with_prefix(folder_path, prefix):
    png_files = []
    for filename in os.listdir(folder_path):
        if filename.lower().startswith(prefix.lower()) and filename.lower().endswith(
            ".png"
        ):
            png_files.append(os.path.join(folder_path, filename))
    return png_files


def save_gif(dataset, hue, path):
    path = path + "/{0}/{1}".format(dataset, hue)
    prefix = "{0}_{1}_".format(dataset, hue)
    image_list = find_png_files_with_prefix(path, prefix)

    images = []
    for image_file in image_list:
        img = Image.open(image_file)
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
