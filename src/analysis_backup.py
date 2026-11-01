
import os
import re
import json
import warnings
from collections import Counter

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.cluster import KMeans

warnings.filterwarnings("ignore")

# --------------------------------------------------
# 1. PROJECT PATHS AND SETTINGS
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "News_Category_Dataset_v3.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

os.makedirs(OUTPUT_DIR, exist_ok=True)

RANDOM_STATE = 42
MAX_DOCUMENTS = 30000
NUMBER_OF_TOPICS = 5
NUMBER_OF_CLUSTERS = 5

sns.set_theme(style="whitegrid")


# --------------------------------------------------
# 2. LOAD DATASET
# --------------------------------------------------

print("\nSTEP 1: Loading dataset...")

if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

df = pd.read_json(DATA_PATH, lines=True)

print("Dataset loaded successfully!")
print("Total records:", len(df))
print("Columns:", list(df.columns))

# Check required columns
required_columns = ["headline", "short_description", "category", "date"]

for column in required_columns:
    if column not in df.columns:
        raise ValueError(f"Required column missing: {column}")

df = df[required_columns].copy()

df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.dropna(subset=["date"])

df["text"] = (
    df["headline"].fillna("").astype(str)
    + " "
    + df["short_description"].fillna("").astype(str)
)

df = df[df["text"].str.strip() != ""].copy()
df["year"] = df["date"].dt.year

print("\nDataset information:")
print(df.info())

print("\nYear range:", df["year"].min(), "-", df["year"].max())


# --------------------------------------------------
# 3. TEXT PREPROCESSING
# --------------------------------------------------

print("\nSTEP 2: Cleaning text...")

stop_words = set(ENGLISH_STOP_WORDS)

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    words = text.split()
    words = [
        word for word in words
        if word not in stop_words and len(word) > 2
    ]

    return " ".join(words)

df["clean_text"] = df["text"].apply(clean_text)

df = df[df["clean_text"].str.strip() != ""].copy()

print("Text preprocessing completed!")
print(df[["text", "clean_text"]].head())


# --------------------------------------------------
# 4. WORD FREQUENCY ANALYSIS
# --------------------------------------------------

print("\nSTEP 3: Performing word frequency analysis...")

all_words = " ".join(df["clean_text"]).split()
word_counts = Counter(all_words)

top_words = word_counts.most_common(20)

frequency_df = pd.DataFrame(
    top_words,
    columns=["Word", "Frequency"]
)

frequency_df.to_csv(
    os.path.join(OUTPUT_DIR, "word_frequency.csv"),
    index=False
)

plt.figure(figsize=(12, 7))
sns.barplot(
    data=frequency_df,
    x="Frequency",
    y="Word"
)
plt.title("Top 20 Most Frequent Words in News Articles")
plt.xlabel("Frequency")
plt.ylabel("Words")
plt.tight_layout()
plt.savefig(
    os.path.join(OUTPUT_DIR, "top_words.png"),
    dpi=300
)
plt.close()

print("Word frequency chart saved!")


# --------------------------------------------------
# 5. YEAR-WISE CATEGORY TREND ANALYSIS
# --------------------------------------------------

print("\nSTEP 4: Analyzing yearly language trends...")

yearly_category = pd.crosstab(
    df["year"],
    df["category"],
    normalize="index"
) * 100

yearly_category.to_csv(
    os.path.join(OUTPUT_DIR, "yearly_category_trends.csv")
)

# Select the 6 most frequent categories overall
top_categories = df["category"].value_counts().head(6).index

trend_data = df[df["category"].isin(top_categories)]

yearly_top = (
    trend_data.groupby(["year", "category"])
    .size()
    .reset_index(name="article_count")
)

yearly_total = df.groupby("year").size().rename("total_articles")

yearly_top = yearly_top.join(
    yearly_total,
    on="year"
)

yearly_top["percentage"] = (
    yearly_top["article_count"] / yearly_top["total_articles"] * 100
)

plt.figure(figsize=(13, 7))

sns.lineplot(
    data=yearly_top,
    x="year",
    y="percentage",
    hue="category",
    marker="o"
)

plt.title("Year-wise News Category Trends")
plt.xlabel("Publication Year")
plt.ylabel("Percentage of Articles")
plt.xticks(sorted(df["year"].unique()), rotation=45)
plt.tight_layout()
plt.savefig(
    os.path.join(OUTPUT_DIR, "yearly_category_trends.png"),
    dpi=300
)
plt.close()

print("Yearly trend chart saved!")


# --------------------------------------------------
# 6. PREPARE DOCUMENT SAMPLE FOR ADVANCED NLP
# --------------------------------------------------

print("\nSTEP 5: Preparing documents for topic modeling...")

if len(df) > MAX_DOCUMENTS:
    analysis_df = df.sample(
        n=MAX_DOCUMENTS,
        random_state=RANDOM_STATE
    ).copy()
else:
    analysis_df = df.copy()

analysis_df = analysis_df.reset_index(drop=True)

print("Documents selected for advanced NLP:", len(analysis_df))


# --------------------------------------------------
# 7. LDA TOPIC MODELING
# --------------------------------------------------

print("\nSTEP 6: Applying LDA topic modeling...")

count_vectorizer = CountVectorizer(
    max_features=5000,
    min_df=5,
    max_df=0.90
)

count_matrix = count_vectorizer.fit_transform(
    analysis_df["clean_text"]
)

lda_model = LatentDirichletAllocation(
    n_components=NUMBER_OF_TOPICS,
    random_state=RANDOM_STATE,
    max_iter=10,
    learning_method="batch"
)

topic_matrix = lda_model.fit_transform(count_matrix)

feature_names = count_vectorizer.get_feature_names_out()

topic_results = []

for topic_index, topic in enumerate(lda_model.components_):
    top_indices = topic.argsort()[-10:][::-1]
    top_terms = [feature_names[i] for i in top_indices]

    topic_results.append({
        "Topic": topic_index + 1,
        "Keywords": ", ".join(top_terms)
    })

topics_df = pd.DataFrame(topic_results)

topics_df.to_csv(
    os.path.join(OUTPUT_DIR, "lda_topics.csv"),
    index=False
)

analysis_df["dominant_topic"] = (
    topic_matrix.argmax(axis=1) + 1
)

analysis_df["dominant_topic_probability"] = (
    topic_matrix.max(axis=1)
)

print("\nDiscovered topics:")
print(topics_df.to_string(index=False))


# --------------------------------------------------
# 8. TOPIC TRENDS OVER TIME
# --------------------------------------------------

print("\nSTEP 7: Analyzing topic trends over time...")

topic_yearly = pd.crosstab(
    analysis_df["year"],
    analysis_df["dominant_topic"],
    normalize="index"
) * 100

topic_yearly.to_csv(
    os.path.join(OUTPUT_DIR, "yearly_topic_trends.csv")
)

plt.figure(figsize=(12, 7))

topic_yearly.plot(
    kind="line",
    marker="o",
    figsize=(12, 7)
)

plt.title("Evolution of LDA Topics Over Time")
plt.xlabel("Year")
plt.ylabel("Percentage of Sampled Articles")
plt.legend(title="Topic")
plt.tight_layout()
plt.savefig(
    os.path.join(OUTPUT_DIR, "topic_trends.png"),
    dpi=300
)
plt.close()

print("Topic trend chart saved!")


# --------------------------------------------------
# 9. K-MEANS DOCUMENT CLUSTERING
# --------------------------------------------------

print("\nSTEP 8: Applying K-Means clustering...")

tfidf_vectorizer = TfidfVectorizer(
    max_features=5000,
    min_df=5,
    max_df=0.90
)

tfidf_matrix = tfidf_vectorizer.fit_transform(
    analysis_df["clean_text"]
)

kmeans = KMeans(
    n_clusters=NUMBER_OF_CLUSTERS,
    random_state=RANDOM_STATE,
    n_init=10
)

analysis_df["cluster"] = kmeans.fit_predict(tfidf_matrix) + 1

terms = tfidf_vectorizer.get_feature_names_out()
cluster_results = []

for cluster_number in range(NUMBER_OF_CLUSTERS):
    center = kmeans.cluster_centers_[cluster_number]
    top_indices = center.argsort()[-10:][::-1]

    top_terms = [terms[i] for i in top_indices]

    cluster_results.append({
        "Cluster": cluster_number + 1,
        "Top_Keywords": ", ".join(top_terms)
    })

cluster_df = pd.DataFrame(cluster_results)

cluster_df.to_csv(
    os.path.join(OUTPUT_DIR, "cluster_keywords.csv"),
    index=False
)

analysis_df.to_csv(
    os.path.join(OUTPUT_DIR, "document_analysis_results.csv"),
    index=False
)

cluster_counts = (
    analysis_df["cluster"]
    .value_counts()
    .sort_index()
    .reset_index()
)

cluster_counts.columns = ["Cluster", "Document_Count"]

plt.figure(figsize=(9, 6))
sns.barplot(
    data=cluster_counts,
    x="Cluster",
    y="Document_Count"
)

plt.title("K-Means Document Clusters")
plt.xlabel("Cluster")
plt.ylabel("Number of Documents")
plt.tight_layout()
plt.savefig(
    os.path.join(OUTPUT_DIR, "cluster_distribution.png"),
    dpi=300
)
plt.close()


# --------------------------------------------------
# 10. SAVE SUMMARY STATISTICS
# --------------------------------------------------

summary = {
    "Total_articles": int(len(df)),
    "Analysis_sample": int(len(analysis_df)),
    "Number_of_categories": int(df["category"].nunique()),
    "Start_year": int(df["year"].min()),
    "End_year": int(df["year"].max()),
    "Number_of_topics": NUMBER_OF_TOPICS,
    "Number_of_clusters": NUMBER_OF_CLUSTERS,
    "Most_frequent_word": word_counts.most_common(1)[0][0]
}

with open(
    os.path.join(OUTPUT_DIR, "analysis_summary.json"),
    "w",
    encoding="utf-8"
) as file:
    json.dump(summary, file, indent=4)

print("\n" + "=" * 50)
print("WEEK 4 NLP ANALYSIS COMPLETED SUCCESSFULLY!")
print("=" * 50)

print("\nSummary:")
for key, value in summary.items():
    print(f"{key}: {value}")

print("\nAll charts and result files are saved in:")
print(OUTPUT_DIR)
