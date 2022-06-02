from distutils.command.clean import clean
from newspaper import Article
import sqlfile

from pathlib import Path
import feedparser
import scrape 
import feeds
import tldextract
import os
import json
from FeatureExtractor import SimpleExtractor
from FeatureExtractor import HandTunedExtractor

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

def get_posts_details(posts=None):
	
	"""
	Take link of posts feed as argument
	"""
	simple_extractor = SimpleExtractor()
	handtuned_extractor = HandTunedExtractor()
	# processed_posts = load_log() #todo, check for headline ver batim maybe as dupe protection
	whitelist = load_whitelist()

	if posts is not None:
		
		post_list = []

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
				# full_text = article.text + article.title + "".join(article.keywords)
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
					# id is (often) a reserved word
				# 	location = location_extractor.extract_location(full_text)
				# 	if location is not None:
				# 		with open('./assets/locations.txt', 'a') as f:
				# 			f.write("countries: " + ",".join(location["features"]["countries"]))
				# 			f.write('\n')
				# 			f.write("states/regions:" + ",".join(location["features"]["regions"]))
				# 			f.write('\n')
				# 			f.write("cities:" + ",".join(location["features"]["cities"]))
				# 			f.write('\n')
				# 			f.write('\n')
					# try: 				
					# 	id = post.id.replace('tag:google.com,2013:googlealerts/feed:','')
					# 	title = post.title
					# 	link = clean_url_link
					# 	domain = domain
					# 	author = ";".join(article.authors) # json.dumps(article.authors)
					# 	time_published = post.published
					# 	keywords =";".join(article.keywords) #json.dumps(article.keywords)
					# 	content = article.text
					# 	content_summary = article.summary
					# 	post_list.append([id, title, link, domain, author, time_published, keywords, content, content_summary])
					# except:
					# 	pass #should this be something more robust? see above on line 108
			# else:
			# 	with open("./assets/newdomains.txt", "a") as f:
			# 		f.write(domain)
			# 		f.write('\n')

		# sqlfile.receive_data(post_list)			
					
			


	else:
		return None


def main():
	feed_url = feeds.urls
	posts = []
	for k in feed_url.values():
		# get_posts_details(rss = k) 
		google_rss = google_rss = feedparser.parse(k)
		post_dict = google_rss.entries

		for post in post_dict:
			posts.append(post)

	get_posts_details(posts)

main()


# with requests.get(clean_url_link, headers=HEADERS, timeout=10) as response:
# 	# Most of the times the encoding is utf-8 but in edge cases
# 	# we set it to ISO-8859-1 when it is present in the HTML header.
# 	if "iso-8859-1" in response.text.lower():
# 		response.encoding = "iso-8859-1"
# 	elif response.encoding == "ISO-8859-1":
# 		response.encoding = "utf-8"

# html_source = response.text.lower()
# article_body = scrape.scrape_html(html_source)