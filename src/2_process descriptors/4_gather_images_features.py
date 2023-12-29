# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity


df = pd.read_csv("data/interim/image_features_by_manga.csv")


# %%
def determine_pca_components(df):
    scaler = StandardScaler()
    scores_scaled = scaler.fit_transform(df.drop(["rank"], axis=1))
    pca = PCA()
    pca.fit(scores_scaled)

    # Get explained variance ratio for each component
    explained_variance_ratio = pca.explained_variance_ratio_

    # Plot the cumulative explained variance to find the elbow point
    cumulative_variance = np.cumsum(explained_variance_ratio)
    plt.plot(range(1, len(cumulative_variance) + 1), cumulative_variance, marker="o")
    plt.xlabel("Number of Components")
    plt.ylabel("Cumulative Explained Variance")
    plt.title("Elbow Method to Find Optimal Number of Components")
    plt.grid(True)
    plt.show()


# %%
determine_pca_components(df)


# %%
def scale_and_pca(df, num_comp):
    scaler = StandardScaler()
    scaled_df = scaler.fit_transform(df.drop(["rank"], axis=1))
    pca = PCA(n_components=num_comp)
    pca_df = pca.fit_transform(scaled_df)
    return pca_df


def get_pca_dataset(df, num_comp):
    pca_array = scale_and_pca(df, num_comp)

    pca_cols = ["image_pca_" + str(i) for i in range(pca_array.shape[1])]
    pca_pd = pd.DataFrame(pca_array, columns=pca_cols)
    pca_df = df[["rank"]].merge(pca_pd, left_index=True, right_index=True)
    return pca_df


# %%
num_comp = 550
pca_df = get_pca_dataset(df, num_comp)
pca_df.to_csv("data/processed/procsessed_features_image_pca.csv", index=False)

# %%
# score_similarities = get_score_similarities(df, num_comp)
# score_similarities.to_csv("data/processed/similarities_score.csv", index=False)
