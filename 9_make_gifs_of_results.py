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
    prefix = "{}_{}_".format(dataset, hue)
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
dataset = "image_pca"
hue = "starting_decade"
path = "data/images/results"
save_gif(dataset, hue, path)


# %%
dataset = "image_pca"
hue = "mal_demographic"
path = "data/images/results"
save_gif(dataset, hue, path)

# %%
