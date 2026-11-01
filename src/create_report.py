
import os
import json
import pandas as pd

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT

# Project paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
REPORT_DIR = os.path.join(BASE_DIR, "report")

os.makedirs(REPORT_DIR, exist_ok=True)

doc = Document()

# Page settings
section = doc.sections[0]
section.top_margin = Inches(0.7)
section.bottom_margin = Inches(0.7)
section.left_margin = Inches(0.8)
section.right_margin = Inches(0.8)

# Default font
styles = doc.styles
styles["Normal"].font.name = "Calibri"
styles["Normal"].font.size = Pt(11)

# Heading styles
for style_name in ["Heading 1", "Heading 2"]:
    styles[style_name].font.name = "Calibri"
    styles[style_name].font.color.rgb = RGBColor(31, 78, 121)

# Load analysis results
with open(os.path.join(OUTPUT_DIR, "analysis_summary.json"), encoding="utf-8") as f:
    summary = json.load(f)

evaluation = pd.read_csv(os.path.join(OUTPUT_DIR, "model_evaluation.csv"))
topics = pd.read_csv(os.path.join(OUTPUT_DIR, "lda_topics.csv"))
clusters = pd.read_csv(os.path.join(OUTPUT_DIR, "cluster_keywords.csv"))

def add_paragraph(text):
    doc.add_paragraph(text)

def add_heading(text, level=1):
    doc.add_heading(text, level=level)

def add_chart(filename, caption):
    path = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(path):
        doc.add_picture(path, width=Inches(6.0))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        p = doc.add_paragraph(caption)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.runs[0].italic = True

def add_table(headers, rows):
    table = doc.add_table(rows=1, cols=len(headers))
    table.style = "Light Shading Accent 1"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    for i, header in enumerate(headers):
        table.rows[0].cells[i].text = str(header)

    for row in rows:
        cells = table.add_row().cells
        for i, value in enumerate(row):
            cells[i].text = str(value)
            cells[i].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER

    doc.add_paragraph()

# ------------------------------------------------
# TITLE PAGE
# ------------------------------------------------

title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title.add_run("\n\n\nADVANCED ANALYSIS AND\nREPORTING OF LANGUAGE TRENDS\nUSING NLP TECHNIQUES")
run.bold = True
run.font.size = Pt(23)
run.font.color.rgb = RGBColor(31, 78, 121)

p = doc.add_paragraph("\n\nWEEK 4 INTERNSHIP PROJECT")
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.runs[0].bold = True
p.runs[0].font.size = Pt(16)

p = doc.add_paragraph(
    "\n\nSubmitted by\n"
    "Arfat Shakil Sherkhan\n\n"
    "B.Tech – Artificial Intelligence and Machine Learning\n"
    "Sanjay Ghodawat University\n\n"
    "Academic Year: 2026–2027"
)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_page_break()

# ------------------------------------------------
# ABSTRACT
# ------------------------------------------------

add_heading("1. Abstract")

add_paragraph(
    "This project focuses on analyzing language trends in news articles "
    "using Natural Language Processing (NLP) techniques. The HuffPost "
    "News Category Dataset was used to identify frequently occurring "
    "words, discover hidden topics, group similar documents and study "
    "changes in news themes over time. Text preprocessing was performed "
    "before applying word frequency analysis, Latent Dirichlet Allocation "
    "(LDA) and K-Means clustering. The analysis covered 209,497 valid "
    "articles, while advanced topic modeling and clustering were performed "
    "on a sample of 30,000 documents. The project demonstrates how NLP "
    "can convert large amounts of unstructured news text into useful "
    "patterns and insights."
)

# ------------------------------------------------
# INTRODUCTION
# ------------------------------------------------

add_heading("2. Introduction")

add_paragraph(
    "News articles contain large amounts of textual information about "
    "politics, society, health, entertainment and other subjects. "
    "Analyzing this information manually is time-consuming. Natural "
    "Language Processing provides techniques that help computers process "
    "human language and discover useful patterns from text."
)

add_paragraph(
    "This project applies NLP methods to understand common words, "
    "identify major topics and examine how the distribution of topics "
    "changes across different years."
)

# ------------------------------------------------
# OBJECTIVES
# ------------------------------------------------

add_heading("3. Project Objectives")

objectives = [
    "To collect and analyze a large news article dataset.",
    "To clean and preprocess textual data.",
    "To identify the most frequently occurring words.",
    "To analyze yearly trends in news categories and topics.",
    "To discover hidden topics using LDA topic modeling.",
    "To group similar news documents using K-Means clustering.",
    "To evaluate the performance of the topic and clustering models."
]

for item in objectives:
    doc.add_paragraph(item, style="List Bullet")

# ------------------------------------------------
# DATASET
# ------------------------------------------------

add_heading("4. Dataset Description")

add_paragraph(
    "The project uses the HuffPost News Category Dataset v3, obtained "
    "from Kaggle. It contains news article information such as headlines, "
    "short descriptions, categories, publication dates, authors and links."
)

add_table(
    ["Dataset detail", "Value"],
    [
        ["Total records loaded", "209,527"],
        ["Valid articles analyzed", str(summary["Total_articles"])],
        ["Number of categories", str(summary["Number_of_categories"])],
        ["Starting year", str(summary["Start_year"])],
        ["Ending year", str(summary["End_year"])],
        ["Advanced analysis sample", str(summary["Analysis_sample"])]
    ]
)

add_paragraph(
    "Dataset source: Kaggle – HuffPost News Category Dataset v3\n"
    "https://www.kaggle.com/datasets/rmisra/news-category-dataset"
)

# ------------------------------------------------
# TECHNOLOGIES
# ------------------------------------------------

add_heading("5. Tools and Technologies Used")

tools_used = [
    "Python 3.12",
    "Pandas and NumPy for data processing",
    "Matplotlib and Seaborn for visualization",
    "Scikit-learn for NLP, LDA and K-Means",
    "TF-IDF and CountVectorizer for text representation",
    "python-docx for report generation"
]

for item in tools_used:
    doc.add_paragraph(item, style="List Bullet")

# ------------------------------------------------
# METHODOLOGY
# ------------------------------------------------

add_heading("6. Methodology")

steps = [
    ("Data loading", "Loaded the JSON dataset using Pandas."),
    ("Text preprocessing", "Converted text to lowercase, removed URLs and non-letter characters, removed English stop words and short tokens."),
    ("Word frequency analysis", "Counted frequently occurring words and visualized the top 20 words."),
    ("Yearly trend analysis", "Calculated yearly proportions of news categories."),
    ("Topic modeling", "Applied LDA with five topics to discover hidden themes in news articles."),
    ("Topic trend analysis", "Studied the yearly distribution of dominant LDA topics."),
    ("Document clustering", "Used TF-IDF features and K-Means to group similar documents into five clusters."),
    ("Model evaluation", "Calculated LDA perplexity and K-Means silhouette score.")
]

for heading, description in steps:
    add_heading(heading, 2)
    add_paragraph(description)

# ------------------------------------------------
# WORD FREQUENCY
# ------------------------------------------------

add_heading("7. Word Frequency Analysis")

add_paragraph(
    "Word frequency analysis identifies the most common words in the "
    "news dataset. The word 'trump' was identified as the most frequent "
    "word, followed by 'new'. Other frequent words included people, "
    "time, photos, day and year."
)

add_chart("top_words.png", "Figure 1: Top 20 most frequent words")

# ------------------------------------------------
# YEARLY TRENDS
# ------------------------------------------------

add_heading("8. Yearly Language and Category Trends")

add_paragraph(
    "Yearly trend analysis was used to examine how the proportions of "
    "different news categories changed over time. The analysis helps "
    "identify variations in the subjects covered by the dataset."
)

add_chart(
    "yearly_category_trends.png",
    "Figure 2: Yearly news category trends"
)

# ------------------------------------------------
# LDA
# ------------------------------------------------

add_heading("9. LDA Topic Modeling")

add_paragraph(
    "Latent Dirichlet Allocation (LDA) is an unsupervised topic modeling "
    "technique. It identifies groups of words that frequently occur "
    "together and uses them to discover hidden themes in documents. "
    "Five topics were identified in this project."
)

topic_rows = []
for _, row in topics.iterrows():
    topic_rows.append([row["Topic"], row["Keywords"]])

add_table(["Topic", "Top keywords"], topic_rows)

add_chart(
    "topic_trends.png",
    "Figure 3: Evolution of LDA topics over time"
)

# ------------------------------------------------
# KMEANS
# ------------------------------------------------

add_heading("10. K-Means Document Clustering")

add_paragraph(
    "K-Means is an unsupervised machine learning algorithm that groups "
    "similar documents into clusters. TF-IDF was used to represent the "
    "documents numerically. Five clusters were generated."
)

cluster_rows = []
for _, row in clusters.iterrows():
    cluster_rows.append([row["Cluster"], row["Top_Keywords"]])

add_table(["Cluster", "Top keywords"], cluster_rows)

add_chart(
    "cluster_distribution.png",
    "Figure 4: Distribution of documents across clusters"
)

# ------------------------------------------------
# EVALUATION
# ------------------------------------------------

add_heading("11. Model Evaluation")

evaluation_rows = []
for _, row in evaluation.iterrows():
    evaluation_rows.append([
        row["Model"],
        row["Evaluation_Metric"],
        f'{float(row["Score"]):.4f}'
    ])

add_table(
    ["Model", "Evaluation metric", "Score"],
    evaluation_rows
)

add_paragraph(
    "The LDA perplexity score was approximately 2637.02. Perplexity "
    "measures how well a topic model predicts unseen word patterns; "
    "lower values can indicate better predictive fit when models are "
    "compared under the same conditions."
)

add_paragraph(
    "The K-Means silhouette score was approximately 0.003. This value "
    "indicates weak separation between the generated clusters. The "
    "documents have overlapping language patterns, so further tuning "
    "and alternative clustering methods may improve the results."
)

# ------------------------------------------------
# FINDINGS
# ------------------------------------------------

add_heading("12. Key Findings")

findings = [
    "The most frequent word in the analyzed dataset was 'trump'.",
    "The LDA model identified five major topics.",
    "The discovered topics included politics, fashion and media, social issues, lifestyle and personal life.",
    "The dataset contained 42 news categories.",
    "The yearly topic chart showed changes in the proportions of topics over time.",
    "K-Means produced five clusters, but the silhouette score indicated weak cluster separation."
]

for item in findings:
    doc.add_paragraph(item, style="List Bullet")

# ------------------------------------------------
# LIMITATIONS
# ------------------------------------------------

add_heading("13. Limitations")

limitations = [
    "Advanced LDA and K-Means analysis used a random sample of 30,000 documents rather than the entire dataset.",
    "The dataset has uneven temporal coverage, which can affect comparisons between years.",
    "Word frequency does not identify the meaning or context of a word.",
    "The K-Means silhouette score indicates that the generated clusters are not clearly separated.",
    "LDA topics require human interpretation based on their keywords."
]

for item in limitations:
    doc.add_paragraph(item, style="List Bullet")

# ------------------------------------------------
# CONCLUSION
# ------------------------------------------------

add_heading("14. Conclusion")

add_paragraph(
    "The project successfully demonstrated the application of Natural "
    "Language Processing techniques to a large news dataset. Word "
    "frequency analysis, yearly trend analysis, LDA topic modeling and "
    "K-Means clustering were used to identify patterns in news articles. "
    "The results revealed frequently occurring words and five major "
    "topics. Model evaluation also highlighted the need for further "
    "improvement in cluster separation. Overall, this project provided "
    "practical experience in text preprocessing, unsupervised learning, "
    "data visualization and analytical reporting."
)

# ------------------------------------------------
# REFERENCES
# ------------------------------------------------

add_heading("15. References")

references = [
    "HuffPost News Category Dataset v3, Kaggle: https://www.kaggle.com/datasets/rmisra/news-category-dataset",
    "Scikit-learn Documentation: https://scikit-learn.org/",
    "Pandas Documentation: https://pandas.pydata.org/docs/",
    "Matplotlib Documentation: https://matplotlib.org/stable/",
    "Seaborn Documentation: https://seaborn.pydata.org/"
]

for item in references:
    doc.add_paragraph(item, style="List Number")

# ------------------------------------------------
# HEADER AND FOOTER
# ------------------------------------------------

for sec in doc.sections:
    footer = sec.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer.add_run(
        "Week 4 NLP Internship Project | Language Trend Analysis"
    )

# Save report
report_path = os.path.join(
    REPORT_DIR,
    "Week4_NLP_Analysis_Report.docx"
)

doc.save(report_path)

print("\n" + "=" * 50)
print("WORD REPORT CREATED SUCCESSFULLY!")
print("=" * 50)
print("Report saved at:")
print(report_path)
