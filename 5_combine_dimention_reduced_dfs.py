# %%
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# %%
doc2vec = pd.read_csv("data/processed/processed_features_doc2vec.csv")
tags = pd.read_csv("data/processed/processed_features_tag_svd.csv")
scores = pd.read_csv("data/processed/processed_features_score_pca.csv")
images = pd.read_csv("data/processed/processed_features_image_pca.csv")

# %%
dataset_list = {
    "doc2vec": {"dataset": doc2vec, "pct": 0.25},
    "tag_svd": {"dataset": tags, "pct": 0.40},
    "score_pca": {"dataset": scores, "pct": 0.05},
    "image_pca": {"dataset": images, "pct": 0.30},
}


def prepare_dataset_list(dataset_list):
    total_cols = 0
    for dataset in dataset_list:
        columns = dataset_list[dataset]["dataset"].shape[1] - 1
        dataset_list[dataset]["cols"] = columns
        total_cols += columns

    print(total_cols)

    for dataset in dataset_list:
        columns = dataset_list[dataset]["cols"]
        pct = dataset_list[dataset]["pct"]
        ratio = (total_cols * pct) / columns
        dataset_list[dataset]["ratio"] = ratio
        print(dataset, dataset_list[dataset]["cols"], ratio)

    return dataset_list


def merge_all_datasets(dataset_list):
    for n, dataset in enumerate(dataset_list):
        df = dataset_list[dataset]["dataset"]
        if n == 0:
            merged_df = df
        else:
            merged_df = pd.merge(merged_df, df, on="rank", how="inner")
    return merged_df


def scale_and_and_ratio_dataset(df, dataset_list):
    data = df.drop(["rank"], axis=1)

    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)
    columns_to_scale = data.columns
    scaled_df = pd.DataFrame(scaled_data, columns=columns_to_scale)

    for dataset in dataset_list:
        ratio = dataset_list[dataset]["ratio"]
        sub_columns = [col for col in scaled_df.columns if col.startswith(dataset)]

        scaled_df[sub_columns] = scaled_df[sub_columns] * ratio

    scaled_df = pd.concat([df[["rank"]], scaled_df], axis=1)

    return scaled_df


# %%
dataset_list = prepare_dataset_list(dataset_list)
merged_df = merge_all_datasets(dataset_list)
scaled_df = scale_and_and_ratio_dataset(merged_df, dataset_list)

# %%
scaled_df
scaled_df.to_csv("data/processed/processed_features_ALL_scaled.csv", index=False)


# %%
def determine_pca_components(df):
    df = pd.DataFrame(scaled_df.drop(["rank"], axis=1))
    pca = PCA(n_components=None)
    pca.fit(df)
    explained_variance = pca.explained_variance_ratio_

    plt.plot(
        np.arange(1, len(explained_variance) + 1),
        np.cumsum(explained_variance),
        marker="o",
    )
    plt.xlabel("Number of Components")
    plt.ylabel("Cumulative Explained Variance")
    plt.title("PCA Elbow Plot")
    plt.xticks(rotation=90)
    plt.grid(True)
    plt.show()


determine_pca_components(scaled_df)

# %%
pca_comp = 625
pca = PCA(n_components=pca_comp)
pca_df = pca.fit_transform(scaled_df.drop(["rank"], axis=1))

columns_pca = ["pca_" + str(x) for x in range(pca_comp)]
pca_df = pd.DataFrame(pca_df, columns=columns_pca)
pca_df = pd.concat([scaled_df[["rank"]], pca_df], axis=1)

# %%
pca_df
pca_df.to_csv("data/processed/processed_features_ALL_pca.csv", index=False)
