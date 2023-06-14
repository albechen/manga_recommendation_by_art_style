# %%
import pandas as pd
from sklearn.manifold import TSNE
import numpy as np

# %%
df = pd.read_csv("data/processed/image_features_by_managa.csv")

# %%
y_df = df[["rank", "pic_count"]]
X_df = df.drop(["rank", "pic_count"], axis=1)

# %%
tsne = TSNE(n_components=2, random_state=42)
tsne_result = tsne.fit_transform(X_df)
tsne_df = pd.DataFrame(tsne_result, columns=["tsne1", "tsne2"])

# %%
result_df = pd.concat([y_df, tsne_df], axis=1)
result_df

# %%
import seaborn as sns
import matplotlib.pyplot as plt

sns.scatterplot(data=tsne_df, x="tsne1", y="tsne2", s=10, alpha=0.4)
plt.xlabel("t-SNE Dimension 1")
plt.ylabel("t-SNE Dimension 2")
plt.title("t-SNE Visualization")
plt.show()


# %%
