# %%
import pandas as pd
from PIL import Image, ImageFile, ImageFont, ImageDraw, ImageOps

ImageFile.LOAD_TRUNCATED_IMAGES = True


# %%
def add_title_to_image(path, text):
    img = Image.open(path)
    height = img.size[1]
    border = int(height * 0.10)
    font_size = int(height * 0.07)

    img = ImageOps.expand(img, border=(0, border, 0, 0), fill="white")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("FONTS/arial.ttf", font_size)
    draw.text((0, 0), text, (0, 0, 0), font=font)
    return img


def scale_image(image, target_width):
    # Calculate the scaling factor to achieve the target width
    scaling_factor = target_width / float(image.size[0])
    # Calculate the new height based on the scaling factor
    target_height = int(float(image.size[1]) * float(scaling_factor))
    # Resize the image
    resized_image = image.resize((target_width, target_height), Image.LANCZOS)
    return resized_image


def stack_images_vertically(images, target_width):
    # Scale each image to have the same width
    scaled_images = [scale_image(img, target_width) for img in images]

    # Get the dimensions of the first scaled image
    width, height = scaled_images[0].size

    # Create a new blank image with the same width but the combined height
    result_image = Image.new("RGBA", (width, sum(img.size[1] for img in scaled_images)))

    # Paste each scaled image onto the result image
    y_offset = 0
    for img in scaled_images:
        result_image.paste(img, (0, y_offset))
        y_offset += img.size[1]

    return result_image


# %%
def get_source_rank_image(result_dict, rank_num):
    rank_str = str(rank_num).zfill(5)
    img_path = "data/images/summary/{}.jpg".format(rank_str)

    first_key, first_value = list(result_dict.items())[0]

    title = first_value["source_title"]
    demographic = first_value["source_demographic"]
    decade = first_value["source_decade"]

    text = "{} - SOURCE: {} - Demographic: {}, Start Decade: {}".format(
        rank_str, title, demographic, decade
    )

    summary_img = add_title_to_image(img_path, text)
    return summary_img


# %%
def get_place_rank_images(result_dict):
    summary_img_list = []
    for rank in result_dict:
        rank = int(rank)
        rank_str = str(rank).zfill(5)
        img_path = "data/images/summary/{}.jpg".format(rank_str)

        similarity_score = round(result_dict[rank]["similarity_score"], 3)
        place = int(result_dict[rank]["place"])
        title = result_dict[rank]["place_title"]
        demographic = result_dict[rank]["place_demographic"]
        decade = result_dict[rank]["place_decade"]

        text = "{} - PLACE:{} - {} - Similarity {}, Demographic: {}, Start Decade: {}".format(
            rank_str, place, title, similarity_score, demographic, decade
        )

        summary_img = add_title_to_image(img_path, text)
        summary_img_list.append(summary_img)
    return summary_img_list


def get_top_similar_summary(rank_num, num_display, df):
    filtered_df = df[df["source_rank"] == rank_num].head(num_display)
    result_dict = filtered_df.set_index("place_rank").to_dict(orient="index")

    source_summary_img = get_source_rank_image(result_dict, rank_num)
    place_summary_imgs = get_place_rank_images(result_dict)

    summary_imgs = [source_summary_img] + place_summary_imgs
    result_img = stack_images_vertically(summary_imgs, 2000)
    return result_img


# %%
top_similar_df = pd.read_csv("data/processed/top_similarties_image_feature.csv")
num_display = 3

# %%
rank_num = 7
vinland_saga_img = get_top_similar_summary(rank_num, num_display, top_similar_df)
vinland_saga_img.save("data/images/results/random_recc/vinland_saga_img.png")

# %%
rank_num = 143
kaichou_maid_img = get_top_similar_summary(rank_num, num_display, top_similar_df)
kaichou_maid_img.save("data/images/results/random_recc/kaichou_maid_img.png")


# %%
rank_num = 76
blue_lock_img = get_top_similar_summary(rank_num, num_display, top_similar_df)
blue_lock_img.save("data/images/results/random_recc/blue_lock_img.png")

# %%
rank_num = 210
paradise_kiss_img = get_top_similar_summary(rank_num, num_display, top_similar_df)
paradise_kiss_img.save("data/images/results/random_recc/paradise_kiss_img.png")

# %%
# test = top_similar_df[['source_rank', 'source_title', 'source_demographic', 'source_decade']]
# filtered_test = test[test["source_demographic"] == "Josei"].drop_duplicates()

# filtered_test.head(50)
