import json
import sqlfile
import feedparser
import scrape 
import feeds
import requests
import tldextract
import summary

# count the rss feed items and log whether all were parsed or if any were skipped and if so which ones

# File locations
HEADERS = {"User-Agent": "Summarizer v2.0"}
HEADLINES_LOG = "./processed_headlines.txt" #headline w/ id
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
	processed_posts = load_log() #todo, check for headline ver batim
	whitelist = load_whitelist()

	if posts is not None:
		
		post_list = []

		# iterating over individual posts
		for post in posts:
			clean_url_link = scrape.clean_url(post.link)
			ext = tldextract.extract(clean_url_link)
			domain = "{}.{}".format(ext.domain, ext.suffix) #example wmar2news.com
			if domain in whitelist:
				# if any post doesn't have information then throw error or maybe replace w/ ""
				try: 
					with requests.get(clean_url_link, headers=HEADERS, timeout=10) as response:
						# Most of the times the encoding is utf-8 but in edge cases
						# we set it to ISO-8859-1 when it is present in the HTML header.
						if "iso-8859-1" in response.text.lower():
							response.encoding = "iso-8859-1"
						elif response.encoding == "ISO-8859-1":
							response.encoding = "utf-8"

					html_source = response.text.lower()
					article_body = scrape.scrape_html(html_source)
					
					id = post.id.replace('tag:google.com,2013:googlealerts/feed:','')
					title = post.title # check headlines for dupes before insert
					link = clean_url_link
					domain = domain
					author = post.author
					time_published = post.published
					content = article_body
					content_summary = ""
					post_list.append([id, title, link, domain, author, time_published, content, content_summary])
				
				except:
					pass #should this be something more robust? see above on line 108
			else:
				with open('newdomains.txt', 'a') as f:
					f.write(domain)
					f.write('\n')

		sqlfile.receive_data(post_list)			
					
			


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
