# %%
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# %%
df_S = pd.read_csv("data/interim/image_features_CVN_S_pca.csv")
df_C = pd.read_csv("data/interim/image_features_CVN_C_pca.csv")

df = df_S.merge(df_C, on=["pic_path", "rank", "pic_name"], how="inner")

# %%
print("X-Y SPLIT")
X_df = df.drop(["pic_path", "rank", "pic_name"], axis=1)
y_df = df[["pic_path", "rank", "pic_name"]]

print("SCALING")
scaler_standard = StandardScaler()
X_scaled = scaler_standard.fit_transform(X_df)


# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Perform PCA on your dataset and obtain the explained variance ratio
# pca.fit(X)  # X is your dataset
pca = PCA(n_components=X_scaled.shape[1])
pca.fit(X_scaled)
explained_var_ratio = pca.explained_variance_ratio_

# Compute the cumulative explained variance ratio
cumulative_var_ratio = np.cumsum(explained_var_ratio)

# Create a scree plot
component_number = np.arange(1, len(explained_var_ratio) + 1)

plt.plot(component_number[400:650], explained_var_ratio[400:650], marker="o")
plt.xlabel("Principal Component")
plt.ylabel("Explained Variance Ratio")
plt.title("Scree Plot")
plt.show()
# %%
# Create a new DataFrame with only the numerical columns
import numpy as np

# Perform PCA


# Calculate the cumulative explained variance ratio
explained_variance_ratio = pca.explained_variance_ratio_
cumulative_explained_variance_ratio = np.cumsum(explained_variance_ratio)

# Print the cumulative explained variance ratio for each number of components
for n, ratio in enumerate(cumulative_explained_variance_ratio, 1):
    print(f"Number of Components: {n}, Cumulative Explained Variance Ratio: {ratio}")


# %%
print("PCA")
pca_comp = 550
pca = PCA(n_components=pca_comp)
X_pca = pca.fit_transform(X_scaled)

print("PCA TO PD DF")
pca_col = ["PCA_" + str(n) for n in range(pca_comp)]
X_pca_df = pd.DataFrame(X_pca, columns=pca_col)

print("MERGING")
merged_df = y_df.join(X_pca_df)
print("SAVING")
merged_df.to_csv("data/interim/image_feature_pca.csv")


# df.to_csv("data/interim/features_pca.csv")

# %%
