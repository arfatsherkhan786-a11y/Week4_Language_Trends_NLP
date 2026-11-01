# Advanced Analysis and Reporting of Language Trends Using NLP Techniques

## Week 4 Internship Project

**Student Name:** Arfat Shakil Sherkhan  
**Degree:** B.Tech – Artificial Intelligence and Machine Learning  
**University:** Sanjay Ghodawat University  
**Academic Year:** 2026–2027

## 1. Project Overview

This project analyzes language trends in news articles using Natural Language Processing (NLP) techniques. It uses the HuffPost News Category Dataset to identify frequently used words, discover hidden topics, analyze category trends over time, and group similar news articles.

## 2. Objectives

- Analyze frequently used words in news articles.
- Identify language and category trends over different years.
- Discover hidden topics using Latent Dirichlet Allocation (LDA).
- Group similar documents using K-Means clustering.
- Evaluate the performance of the NLP models.
- Generate charts, CSV files, and a final analytical report.

## 3. Dataset

**Dataset:** News Category Dataset v3  
**Source:** Kaggle – https://www.kaggle.com/datasets/rmisra/news-category-dataset

The dataset contains news articles from HuffPost, including headlines, short descriptions, categories, and publication dates.

- Total valid articles analyzed: 209,497
- Number of categories: 42
- Date range: 2012–2022
- Advanced model analysis sample: 30,000 articles

## 4. Technologies Used

- Python 3.12
- Pandas and NumPy
- NLTK
- Scikit-learn
- Matplotlib
- Seaborn
- WordCloud
- Jupyter/VS Code or Python environment

## 5. Methodology

1. Dataset collection and loading.
2. Data cleaning and preprocessing.
3. Text normalization and stopword removal.
4. Word frequency analysis.
5. Yearly category trend analysis.
6. Topic modeling using LDA.
7. Document clustering using K-Means.
8. Model evaluation.
9. Visualization and report generation.

## 6. Key Results

- Analyzed 209,497 valid news articles.
- Identified 42 news categories.
- Found the most frequent word as "trump" in the analyzed dataset.
- Discovered 5 topics using LDA.
- Created 5 clusters using K-Means.
- LDA perplexity: 2637.02.
- K-Means silhouette score: 0.003.

The low silhouette score indicates weak separation between clusters and is considered a limitation of the current clustering approach.

## 7. Project Outputs

The `outputs` folder contains:

- Word frequency analysis
- Yearly category trends
- LDA topic results
- Yearly topic trends
- K-Means cluster keywords
- Cluster distribution chart
- Model evaluation metrics
- Document analysis results
- Analysis summary

## 8. How to Run the Project

1. Install Python 3.12.
2. Download the dataset from Kaggle.
3. Extract the dataset into the `data` folder.
4. Install the required libraries:

```bash
pip install -r requirements.txt
```

5. Run the analysis:

```bash
python src/analysis.py
```

6. Run the report generator:

```bash
python src/create_report.py
```

## 9. Conclusion

This project demonstrates how NLP techniques can be used to analyze large collections of news articles. Word frequency analysis, yearly trend analysis, topic modeling, and clustering help identify patterns in news content. The project also demonstrates the importance of evaluating model performance and understanding limitations.

## 10. References

- HuffPost News Category Dataset v3 – Kaggle.
- Scikit-learn Documentation – https://scikit-learn.org/
- NLTK Documentation – https://www.nltk.org/
- Pandas Documentation – https://pandas.pydata.org/
