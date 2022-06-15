import feedparser
import pull_internet_data.feeds as feeds

def get_posts_details(posts=None):
    return


def main(url_label):
	feed_url = feeds.url_label
	posts = []
	for label, url in feed_url.items():
		print(f"fetching {label}")
		google_rss = google_rss = feedparser.parse(url)
		posts.extend(google_rss.entries)
	
	print(len(posts), "entries")
	get_posts_details(posts)

if __name__ == "__main__": #pattern for fetching positional arguments
    import sys
    _, *args = sys.argv
    main(args[0])