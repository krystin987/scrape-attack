import zipfile
import feedparser
import tldextract
import os
import json
import pull_internet_data.scrape as scrape 
import pull_internet_data.feeds as feeds
from pull_internet_data.FeatureExtractor import SimpleExtractor
from pull_internet_data.FeatureExtractor import HandTunedExtractor

from distutils.command.clean import clean
from newspaper import Article
from datetime import datetime
from pathlib import Path
from zipfile import ZipFile


# count the rss feed items and log whether all were parsed or if any were skipped and if so which ones

# File locations
HEADERS = {"User-Agent": "Summarizer v2.0"}
HEADLINES_LOG = "./assets/processed_headlines.txt" #headline w/ id
WHITELIST_FILE = "./assets/whitelist.txt"
ERROR_LOG = "./error.log"



def load_whitelist():
    """Reads the whitelist.

    Returns
    -------
    list
        A list of domains that are confirmed to have an 'article' tag.

    """

    with open(WHITELIST_FILE, "r", encoding="utf-8") as log_file:
        return log_file.read().splitlines()


def load_log():
    """Reads the processed posts log file and creates it if it doesn't exist.

    Returns
    -------
    list
        A list of Reddit posts ids.

    """

    try:
        with open(HEADLINES_LOG, "r", encoding="utf-8") as log_file:
            return log_file.read().splitlines()

    except FileNotFoundError:
        with open(HEADLINES_LOG, "a", encoding="utf-8") as log_file:
            return []


def update_log(post_id):
    """Updates the processed posts log with the given post id.

    Parameters
    ----------
    post_id : str
        A Reddit post id.

    """

    with open(HEADLINES_LOG, "a", encoding="utf-8") as log_file:
        log_file.write("{}\n".format(post_id))


def log_error(error_message):
    """Updates the error log.

    Parameters
    ----------
    error_message : str
        A string containing the faulty url and the exception message.

    """

    with open(ERROR_LOG, "a", encoding="utf-8") as log_file:
        log_file.write("{}\n".format(error_message))

def zipdir(path, ziph):
	for root, dirs, files in os.walk(path):
		for file in files:
			ziph.write(os.path.join(root, file))

def get_posts_details(posts=None):
	
	"""
	Take link of posts feed as argument
	"""
	simple_extractor = SimpleExtractor()
	handtuned_extractor = HandTunedExtractor()
	# processed_posts = load_log() #todo, check for headline ver batim maybe as dupe protection
	whitelist = load_whitelist()

	if posts is not None:
		
		# iterating over individual posts
		for post in posts:
			article_id = post.id.replace("tag:google.com,2013:googlealerts/feed:","")
			article_dir = Path(f"./incoming_web_data/{article_id}")
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
				nlp_first_check = simple_extractor.analyze_body(article.summary)

				if not nlp_first_check["features"]['dog']:
					with open("./assets/url_unrelated_keywords.txt", "a") as f:
						f.write(clean_url_link)
						f.write("\n")

				else:
					(article_dir / "content.txt").write_text(
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
					(article_dir / "metadata.json").open("w")
					)
			else:
				with open("./assets/new_domains.txt", "a") as f:
						f.write(clean_url_link)
						f.write("\n")

		time_of_day = "pm" if datetime.now().hour > 12 else "am"
		todays_date = datetime.now().strftime(f"%Y_%m_%d_{time_of_day}")
		path = Path(f"./incoming_web_data_zips/")
		path.mkdir(exist_ok=True)

		zipf = ZipFile(f"./incoming_web_data_zips/rss_run_{todays_date}.zip", "w", zipfile.ZIP_DEFLATED)
		zipdir("./incoming_web_data", zipf)
		zipf.close()

	else:
		return None


def main():
	feed_url = feeds.urls
	posts = []
	for label, url in feed_url.items():
		print(f"fetching {label}")
		google_rss = google_rss = feedparser.parse(url)
		posts.extend(google_rss.entries)
	
	print(len(posts), "entries")
	get_posts_details(posts)

if __name__ == "__main__": #pattern for fetching positional arguments
    main()
