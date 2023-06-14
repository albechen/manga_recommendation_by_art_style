# %%
import pandas as pd
import numpy as np

# %%
df = pd.read_csv("data/processed/image_features_by_managa.csv")

# %%
y_df = df[["rank", "pic_count"]]
X_df = df.drop(["rank", "pic_count"], axis=1)

# %%
rank_list = y_df["rank"].to_list()
# %%
x_array = np.array(X_df)
# %%
from scipy.spatial.distance import cosine

manga_count = len(rank_list)
similarity_matrix = np.zeros((manga_count, manga_count))

for i in range(manga_count):
    print(i, i / manga_count)
    for j in range(i + 1, manga_count):
        similarity = 1 - cosine(x_array[i], x_array[j])
        similarity_matrix[i, j] = similarity
        similarity_matrix[j, i] = similarity

# %%
similarity_df = pd.DataFrame(similarity_matrix, index=rank_list, columns=rank_list)
similarity_df

# %%
similarity_df.to_csv("data/processed/image_feature_similarity.csv")
# %%
