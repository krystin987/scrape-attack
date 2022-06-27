import os
import json
import zipfile
import feedparser
import tldextract
import pull_internet_data.scrape as scrape 
import text_parser.get_keywords as get_keywords
import text_parser.html_to_kwic as kwic
import text_parser.html_to_freq as freq

from pathlib import Path
from zipfile import ZipFile
from datetime import datetime
from newspaper import Article
from pull_internet_data.FeatureExtractor import SimpleExtractor



RSS_FEEDS = "./rss_feeds.json"
WHITELIST_FILE = "./assets/whitelist.txt"

def load_whitelist():
    with open(WHITELIST_FILE, "r", encoding="utf-8") as log_file:
        return log_file.read().splitlines()

def zipdir(path, ziph):
	for root, dirs, files in os.walk(path):
		for file in files:
			ziph.write(os.path.join(root, file))

def get_posts_details(posts=None,topic=None):
    whitelist = load_whitelist()
    if posts is not None:
        for post in posts:
            article_id = post.id.replace("tag:google.com,2013:googlealerts/feed:","")
            article_dir = Path(f"./incoming_web_data/{topic}/{article_id}")
            if article_dir.exists():
                continue
            article_dir.mkdir(parents=True)
            clean_url_link = scrape.clean_url(post.link)
            ext = tldextract.extract(clean_url_link)
            domain = "{}.{}".format(ext.domain, ext.suffix) #example wmar2news.com
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
                with open("./assets/new_domains.txt", "a") as f:
                    f.write(clean_url_link)
                    f.write("\n")        
        time_of_day = "pm" if datetime.now().hour > 12 else "am"
        todays_date = datetime.now().strftime(f"%Y_%m_%d_{time_of_day}")
        path = Path(f"./incoming_web_data_zips/")
        path.mkdir(exist_ok=True)

        zipf = ZipFile(f"./incoming_web_data_zips/{topic}_{todays_date}.zip", "w", zipfile.ZIP_DEFLATED)
        zipdir("./incoming_web_data", zipf)
        zipf.close()
    else:
        return None

def fetch_urls(rss_topic):

    f = open(RSS_FEEDS)
    data = json.load(f)

    feed_url = data[f"{rss_topic}"]
    posts = []
    for label, url in feed_url.items():
        print(f"fetching {label}")
        google_rss = google_rss = feedparser.parse(url)
        posts.extend(google_rss.entries)

    print(len(posts), "entries")
    f.close()
    return posts

#load the json
def main(rss_topic):
    posts = fetch_urls(rss_topic)
    get_posts_details(posts, rss_topic)

if __name__ == "__main__": #pattern for fetching positional arguments
    import sys
    _, *args = sys.argv
    main(args[0])