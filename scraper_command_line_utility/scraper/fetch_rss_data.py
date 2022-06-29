from datetime import datetime
from pathlib import Path
import json
import os
import zipfile

import feedparser
import tldextract

from .paths import *

from newspaper import Article
from .pull_internet_data.FeatureExtractor import SimpleExtractor
from .pull_internet_data import scrape
from .text_parser import get_keywords
from .text_parser import html_to_freq as freq
from .text_parser import html_to_kwic as kwic



def extract_article_id(hint):
    return hint.replace("tag:google.com,2013:googlealerts/feed:", "")


def get_posts_details(posts=None, topic=None):
    if not posts:
        return  # returns None when nothing is given
    whitelist = load_whitelist()
    for post in posts:
        article_id = extract_article_id(post.id)
        article_dir = CACHE_DIR / f"incoming_web_data/{topic}/{article_id}"
        if article_dir.exists():
            print("Skipping", article_id)
            continue
        article_dir.mkdir(parents=True)
        clean_url_link = scrape.clean_url(post.link)
        ext = tldextract.extract(clean_url_link)
        domain = "{}.{}".format(ext.domain, ext.suffix)  # example wmar2news.com
        if domain in whitelist:
            article = Article(clean_url_link, language="en")
            article.download()
            article.parse()
            article.nlp()
            kwic.transform_html_to_kwic(article.html, article_id, clean_url_link, topic)
            freq.frequency_html(article.text, article_id, clean_url_link, topic)
            (article_dir / f"content-{article_id}.txt").write_text(
                article.text
            )
            json.dump(
                {
                    "article_id": article_id,
                    "keywords": article.keywords,
                    "title": article.title,
                    "url": clean_url_link,
                    "domain": domain,
                    "authors": article.authors,
                    "summary": article.summary
                },
                (article_dir / f"metadata-{article_id}.json").open("w")
            )
        else:
            with (CONFIG_DIR / "new_domains.txt").open("a") as f:
                f.write(clean_url_link)
                f.write("\n")
    path = CACHE_DIR / "incoming_web_data_zips"
    path.mkdir(exist_ok=True)

    with zipfile.ZipFile(CACHE_DIR / f"incoming_web_data_zips/{topic}_{datetime.now():%Y_%m_%d_%p}.zip",
                         "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(CACHE_DIR / "incoming_web_data"):
            for file in files:
                zf.write(os.path.join(root, file))


def fetch_urls(rss_topic, path=CONFIG_DIR / "rss_feeds.json"):
    path = Path(path)
    data = json.load(path.open())

    feed_url = data[f"{rss_topic}"]
    posts = []
    for label, url in feed_url.items():
        print(f"fetching {label}")
        google_rss = feedparser.parse(url)
        posts.extend(google_rss.entries)

    print(len(posts), "entries")
    return posts
