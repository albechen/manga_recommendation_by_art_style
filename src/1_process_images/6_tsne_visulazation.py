# %%
import pandas as pd
from sklearn.manifold import TSNE
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# %%
df = pd.read_csv("data/processed/image_features_by_managa.csv")

# %%
y_df = df[["rank", "pic_count"]]
X_df = df.drop(["rank", "pic_count"], axis=1)

# %%
k_values = [n * 25 for n in range(20, 40)]

# Compute the within-cluster sum of squares (WCSS) for each value of k
wcss = []
for k in k_values:
    print(k)
    kmeans = KMeans(n_clusters=k, n_init="auto")
    kmeans.fit(X_df)
    wcss.append(kmeans.inertia_)

# Plot the WCSS values
plt.plot(k_values, wcss)
plt.xlabel("Number of Clusters (k)")
plt.ylabel("Within-Cluster Sum of Squares (WCSS)")
plt.title("Elbow Method")
plt.show()

# %%
tsne = TSNE(n_components=2, random_state=42)
tsne_result = tsne.fit_transform(X_df)
tsne_df = pd.DataFrame(tsne_result, columns=["tsne1", "tsne2"])

# %%
result_df = pd.concat([y_df, tsne_df], axis=1)
result_df

# %%
k_values = [n * 5 for n in range(1, 10)]

# Compute the within-cluster sum of squares (WCSS) for each value of k
wcss = []
for k in k_values:
    kmeans = KMeans(n_clusters=k, n_init="auto")
    kmeans.fit(tsne_df)
    wcss.append(kmeans.inertia_)

# Plot the WCSS values
plt.plot(k_values, wcss)
plt.xlabel("Number of Clusters (k)")
plt.ylabel("Within-Cluster Sum of Squares (WCSS)")
plt.title("Elbow Method")
plt.show()

# %%
kmeans = KMeans(n_clusters=20, n_init="auto")
test = kmeans.fit_predict(tsne_df)
result_df["cluster"] = test
result_df

# %%
sns.scatterplot(data=result_df, x="tsne1", y="tsne2", hue="cluster", s=10, alpha=0.3)
plt.xlabel("t-SNE Dimension 1")
plt.ylabel("t-SNE Dimension 2")
plt.title("t-SNE Visualization")
plt.show()


# %%
