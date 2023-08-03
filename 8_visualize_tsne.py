# %%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# %%
dataset_list = [
    "all_pca",
    "all_scale",
    "doc2vec",
    "tag_svd",
    "score_pca",
    "image_pca",
]

df = pd.read_csv("data/processed/final_tsne_and_descriptions.csv")
df


# %%
def visualize_tsne_by_hue(df, data_col, hue_col):
    cols = [data_col + "_" + str(x) for x in range(2)]
    temp_df = df.copy()[[hue_col] + cols]
    temp_df[hue_col] = temp_df[hue_col].astype("category")

    sns.scatterplot(data=temp_df, x=cols[0], y=cols[1], hue=hue_col, alpha=0.3, s=10)
    plt.legend(title=hue_col, bbox_to_anchor=(1, 1), loc="upper left")
    plt.title("TSNE " + data_col + " by " + hue_col)
    plt.xlabel("TSNE_0")
    plt.ylabel("TSNE_1")
    plt.show()


def visualize_tsne_individual_hue(df, dataset_name, hue_col):
    hue_list = list(set(df[hue_col].dropna().tolist()))
    hue_list.sort()
    for hue in hue_list:
        visualize_tsne_by_hue(df[df[hue_col] == hue], dataset_name, hue_col)


# %%
dataset_name = "image_pca"
visualize_tsne_by_hue(df, dataset_name, "mal_demographic")
visualize_tsne_by_hue(df, dataset_name, "starting_decade")
visualize_tsne_by_hue(df, dataset_name, "mean_score")

# %%
dataset_name = "image_pca"
visualize_tsne_individual_hue(df, dataset_name, "mal_demographic")
visualize_tsne_individual_hue(df, dataset_name, "starting_decade")

# %%
dataset_name = "tag_svd"
visualize_tsne_by_hue(df, dataset_name, "mal_demographic")
visualize_tsne_by_hue(df, dataset_name, "starting_decade")
visualize_tsne_by_hue(df, dataset_name, "mean_score")

# %%
dataset_name = "tag_svd"
visualize_tsne_individual_hue(df, dataset_name, "mal_demographic")
visualize_tsne_individual_hue(df, dataset_name, "starting_decade")

# %%
dataset_name = "doc2vec"
visualize_tsne_by_hue(df, dataset_name, "mal_demographic")
visualize_tsne_by_hue(df, dataset_name, "starting_decade")
visualize_tsne_by_hue(df, dataset_name, "mean_score")

# %%
dataset_name = "doc2vec"
visualize_tsne_individual_hue(df, dataset_name, "mal_demographic")
visualize_tsne_individual_hue(df, dataset_name, "starting_decade")

# %%
