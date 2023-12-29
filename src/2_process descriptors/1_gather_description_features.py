# %%
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from gensim.models.doc2vec import TaggedDocument, Doc2Vec

df = pd.read_csv("data/interim/manga_site_features_combined.csv")


# %%
def preprocess_text(text):
    text = str(text)
    text = text.lower()
    text = re.sub(r"[^a-zA-Z]", " ", text)
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words("english"))
    tokens = [token for token in tokens if token not in stop_words]
    return tokens


def preprocess_descriptions(df):
    desc_list = df["ani_description"].tolist()

    preprocessed_data = [preprocess_text(doc) for doc in desc_list]
    tagged_data = [
        TaggedDocument(words=doc, tags=[str(idx)])
        for idx, doc in enumerate(preprocessed_data)
    ]
    return tagged_data


def model_doc2vec_vectors(tagged_data):
    model = Doc2Vec(vector_size=100, min_count=2, epochs=100)
    model.build_vocab(tagged_data)
    model.train(tagged_data, total_examples=model.corpus_count, epochs=model.epochs)

    rank_list = df["rank"].tolist()
    total_ranks = len(rank_list)

    doc_vectors = [model.dv[str(idx)] for idx in range(total_ranks)]
    doc_vectors = [np.array(vec).reshape(1, -1) for vec in doc_vectors]

    return doc_vectors


def get_doc2vec_dataset(df):
    tagged_data = preprocess_descriptions(df)
    doc_vectors = model_doc2vec_vectors(tagged_data)

    doc_vectors = [x[0] for x in doc_vectors]
    cols = ["doc2vec_" + str(i) for i in range(len(doc_vectors[0]))]

    vector_pd = pd.DataFrame(doc_vectors, columns=cols)
    vector_pd = df[["rank"]].merge(vector_pd, left_index=True, right_index=True)
    return vector_pd


def calculate_similarities_each_doc(doc_vectors):
    total_ranks = len(doc_vectors)

    similarities = np.zeros((total_ranks, total_ranks))
    for i in range(total_ranks):
        print(i)
        similarities[i, i] = 1
        for j in range(i + 1, total_ranks):
            doc1 = doc_vectors[i]
            doc2 = doc_vectors[j]
            similarity_value = cosine_similarity(doc1, doc2)
            similarities[i, j] = similarity_value
            similarities[j, i] = similarity_value

    return similarities


def get_description_similarities(df):
    tagged_data = preprocess_descriptions(df)
    doc_vectors = model_doc2vec_vectors(tagged_data)
    similarities = calculate_similarities_each_doc(doc_vectors)

    rank_list = df["rank"].tolist()
    similarities_df = pd.DataFrame(similarities, columns=rank_list, index=rank_list)
    similarities_df.reset_index(inplace=True)
    similarities_df.rename(columns={"index": "rank"}, inplace=True)
    return similarities_df


# %%
tag_df = preprocess_descriptions(df)

plt.hist([len(n.words) for n in tag_df], bins=40, color="blue", edgecolor="black")
plt.show()

# %%
# tagged_data = preprocess_descriptions(df)
# doc_vectors = model_doc2vec_vectors(tagged_data)
# similarities = calculate_similarities_each_doc(doc_vectors[:5])

# %%
vector_pd = get_doc2vec_dataset(df)
vector_pd.to_csv("data/processed/processed_features_doc2vec.csv", index=False)

# %%
# similarities_df = get_description_similarities(df)
# similarities_df.to_csv("data/processed/similarities_description.csv", index=False)

# %%
