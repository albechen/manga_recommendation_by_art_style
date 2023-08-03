# %%
import pandas as pd
from sklearn.manifold import TSNE

# %%
doc2vec = pd.read_csv("data/processed/processed_features_doc2vec.csv")
tags = pd.read_csv("data/processed/processed_features_tag_svd.csv")
scores = pd.read_csv("data/processed/processed_features_score_pca.csv")
images = pd.read_csv("data/processed/processed_features_image_pca.csv")

all_pca = pd.read_csv("data/processed/processed_features_ALL_pca.csv")
all_scale = pd.read_csv("data/processed/processed_features_ALL_scaled.csv")

# %%
dataset_list = {
    "all_pca": all_pca,
    "all_scale": all_scale,
    "doc2vec": doc2vec,
    "tag_svd": tags,
    "score_pca": scores,
    "image_pca": images,
}


# %%
def get_all_tsne_datasets(dataset_list):
    for n, dataset in enumerate(dataset_list):
        print(dataset)
        df = dataset_list[dataset]

        tsne = TSNE(n_components=2, random_state=42)
        tsne_df = tsne.fit_transform(df.drop(["rank"], axis=1))

        dataset_col = [dataset + "_" + str(x) for x in range(2)]
        df_tsne = pd.DataFrame(tsne_df, columns=dataset_col)
        df_tsne = pd.concat([df[["rank"]], df_tsne], axis=1)

        if n == 0:
            final_tsne = df_tsne
        else:
            final_tsne = pd.merge(final_tsne, df_tsne, on="rank", how="inner")

    return final_tsne


# %%
final_tsne = get_all_tsne_datasets(dataset_list)

# %%
final_tsne.to_csv("data/processed/final_tsne_per_manga.csv", index=False)
final_tsne
# %%
