# %%
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import glob
import gc


# %%
def collect_all_csv(path, file_name):
    csv_files = glob.glob(path + file_name + "/*.csv")
    dfs = []

    for file in csv_files:
        print(file)
        df = pd.read_csv(file)
        dfs.append(df)

    print("CONCATING")
    combined_df = pd.concat(dfs)
    print("SAVING CSV")
    combined_df.to_csv(path + file_name + ".csv", index=False)


# %%
def scale_and_pca(path, file_name, output_path, pca_comp):
    print("LOADING")
    df = pd.read_csv(path + file_name + ".csv")

    print("X-Y SPLIT")
    X_df = df.drop(["pic_path", "rank", "pic_name"], axis=1)
    y_df = df[["pic_path", "rank", "pic_name"]]

    print("SCALING")
    scaler_standard = StandardScaler()
    X_df = scaler_standard.fit_transform(X_df)

    print("PCA")
    pca = PCA(n_components=pca_comp)
    X_df = pca.fit_transform(X_df)

    print("PCA TO PD DF")
    initial = file_name[-1]
    pca_col = [initial + str(n) for n in range(pca_comp)]
    X_df = pd.DataFrame(X_df, columns=pca_col)

    print("MERGING")
    merged_df = y_df.join(X_df)
    print("SAVING")
    merged_df.to_csv(output_path + file_name + "_pca.csv")


# %%
path = "data/raw/"
file_name = "image_features_CVN_S"
output_path = "data/interim/"
pca_comp = 500
# collect_all_csv(path, file_name)
scale_and_pca(path, file_name, output_path, pca_comp)

# %%
path = "data/raw/"
file_name = "image_features_CVN_C"
output_path = "data/interim/"
pca_comp = 500
# collect_all_csv(path, file_name)
scale_and_pca(path, file_name, output_path, pca_comp)

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

path = "data/raw/"
file_name = "image_features_CVN_C"
print("LOADING")
df = pd.read_csv(path + file_name + ".csv")

print("X-Y SPLIT")
X_df = df.drop(["pic_path", "rank", "pic_name"], axis=1)
y_df = df[["pic_path", "rank", "pic_name"]]

# %%
del df
gc.collect()

# %%
print("SCALING")
scaler_standard = StandardScaler()
X_df = scaler_standard.fit_transform(X_df)

# %%
# Perform PCA on your dataset and obtain the explained variance ratio
# pca.fit(X)  # X is your dataset
pca = PCA(n_components=4500)
pca.fit(X_df)

# %%
explained_var_ratio = pca.explained_variance_ratio_

# Compute the cumulative explained variance ratio
cumulative_var_ratio = np.cumsum(explained_var_ratio)

# Create a scree plot
component_number = np.arange(1, len(explained_var_ratio) + 1)

# %%
plt.plot(component_number, explained_var_ratio, marker="o")
plt.xlabel("Principal Component")
plt.ylabel("Explained Variance Ratio")
plt.title("Scree Plot")
plt.show()

# %%
plt.plot(component_number[50:2000], explained_var_ratio[50:2000], marker="o")
plt.xlabel("Principal Component")
plt.ylabel("Explained Variance Ratio")
plt.title("Scree Plot")
plt.show()

# %%
plt.plot(component_number[300:1000], explained_var_ratio[300:1000], marker="o")
plt.xlabel("Principal Component")
plt.ylabel("Explained Variance Ratio")
plt.title("Scree Plot")
plt.show()


# %%
plt.plot(component_number[30:700], explained_var_ratio[30:700], marker="o")
plt.xlabel("Principal Component")
plt.ylabel("Explained Variance Ratio")
plt.title("Scree Plot")
plt.show()

# %%
# Calculate the cumulative explained variance ratio
explained_variance_ratio = pca.explained_variance_ratio_
cumulative_explained_variance_ratio = np.cumsum(explained_variance_ratio)

# Print the cumulative explained variance ratio for each number of components
for n, ratio in enumerate(cumulative_explained_variance_ratio, 1):
    print(f"Number of Components: {n}, Cumulative Explained Variance Ratio: {ratio}")

# %%
for n, ratio in enumerate(explained_variance_ratio, 1):
    print(f"Number of Components: {n}, Explained Variance Ratio: {ratio}")

# %%
# check memorey
import psutil

psutil.virtual_memory().available / (1024 * 1024 * 1024)
