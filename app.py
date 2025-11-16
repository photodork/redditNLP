import streamlit as st
import pandas as pd
import requests, time, random, re
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import seaborn as sns
import matplotlib.pyplot as plt

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120 Safari/537.36"}

def get_post_urls(query, limit=3):
    url = f"https://old.reddit.com/search/?q={query.replace(' ', '+')}"
    html = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html, "html.parser")
    urls = [a["href"] for a in soup.select("a.search-title")][:limit]
    return urls

def get_comments_from_post(post_url, max_comments=20):
    html = requests.get(post_url, headers=headers).text
    soup = BeautifulSoup(html, "html.parser")
    comments = []
    for entry in soup.select("div.entry"):
        md = entry.find("div", class_="md")
        if md:
            text = md.get_text(strip=True)
            if len(text.split()) > 4:
                comments.append(text)
        if len(comments) >= max_comments:
            break
    return comments

def scrape_reddit_comments(query, posts_limit=3, comments_limit=20):
    all_comments = []
    post_urls = get_post_urls(query, limit=posts_limit)
    for url in post_urls:
        comments = get_comments_from_post(url, max_comments=comments_limit)
        all_comments.extend(comments)
        time.sleep(random.uniform(1, 2))
    return all_comments

def clean_text(text):
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    return text.lower().strip()

st.title("📊 Reddit Sentiment Analyzer")

query = st.text_input("Enter a topic:", "budget 2025")

if st.button("Analyze"):
    st.write("⏳ Scraping Reddit...")
    comments = scrape_reddit_comments(query)

    if not comments:
        st.warning("No comments found!")
        st.stop()

    df = pd.DataFrame({"comment": comments})
    df["clean"] = df["comment"].apply(clean_text)

    analyzer = SentimentIntensityAnalyzer()

    def get_sentiment(text):
        score = analyzer.polarity_scores(text)["compound"]
        if score > 0.05: return "Positive"
        elif score < -0.05: return "Negative"
        else: return "Neutral"

    df["sentiment"] = df["clean"].apply(get_sentiment)
    st.write(df.head())

    sentiment_counts = df["sentiment"].value_counts()

    fig, ax = plt.subplots(figsize=(5, 3))
    sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, ax=ax)
    st.pyplot(fig)

    st.success("Done!")
