from distutils.command.clean import clean
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

ARTICLE_MINIMUM_LENGTH = 650


def scrape_html(html_text):
    # Very often the text between tags comes together, we add an artificial newline to each common tag.
    for item in ["</p>", "</blockquote>", "</div>", "</h3>", "<br>"]:
        html_source = html_text.replace(item, item+"\n")

    # We create a BeautifulSOup object and remove the unnecessary tags.
    soup = BeautifulSoup(html_source, "html5lib")

    # We remove some tags that add noise.
    [tag.extract() for tag in soup.find_all(
        ["script", "img", "ol", "ul", "time", "h1", "h2", "h3", "iframe", "style", "form", "footer", "figcaption", "svg", "header"])]

    # These class names/ids are known to add noise or duplicate text to the article.
    noisy_names = ["image", "img", "video", "subheadline", "editor", "fondea", "resumen", "tags", "sidebar", "comment",
                   "entry-title", "breaking_content", "pie", "tract", "caption", "tweet", "expert", "previous", "next",
                   "compartir", "rightbar", "mas", "copyright", "instagram-media", "cookie", "paywall", "mainlist", "sitelist", "svg"]

    for tag in soup.find_all("div"):

        try:
            tag_id = tag["id"].lower()

            for item in noisy_names:
                if item in tag_id:
                    tag.extract()
        except:
            pass

    for tag in soup.find_all(["div", "p", "blockquote"]):

        try:
            tag_class = "".join(tag["class"]).lower()

            for item in noisy_names:
                if item in tag_class:
                    tag.extract()
        except:
            pass

    # These names commonly hold the article text.
    common_names = ["artic", "summary", "cont", "note", "cuerpo", "body"]

    article_body = ""

    # Sometimes we have more than one article tag. We are going to grab the longest one.
    for article_tag in soup.find_all("article"):

        # if len(article_tag.text) >= len(article_body):
        article_body = article_tag.text
        article_body = " ".join(article_body.split())

    # The article is too short, let's try to find it in another tag.
    # if len(article_body) <= ARTICLE_MINIMUM_LENGTH:

    # for tag in soup.find_all(["div", "section"]):
    #     try:
    #         tag_id = tag["id"].lower()

    #         for item in common_names:
    #             if item in tag_id:
    #                 # We guarantee to get the longest div.
    #                 if len(tag.text) >= len(article_body):
    #                     article_body = tag.text.strip()
    #     except:
    #         pass

    # The article is still too short, let's try one more time.
    # if len(article_body) <= ARTICLE_MINIMUM_LENGTH:

    # for tag in soup.find_all(["div", "section"]):

    #     try:
    #         tag_class = "".join(tag["class"]).lower()

    #         for item in common_names:
    #             if item in tag_class:
    #                 # We guarantee to get the longest div.
    #                 if len(tag.text) >= len(article_body):
    #                     article_body = tag.text.strip()
    #     except:
    #         pass

    return article_body
    

def get_summary(text):
    return text

def clean_url(url):
    url = re.sub(r'.*url=',"",url)
    url = re.sub(r'[&].*$',"",url)
    return url

    # Then we extract the title and the article tags.
    # article_title = soup.find("title").text.replace("\n", " ").strip()

    # If our title is too short we fallback to the first h1 tag.
    # if len(article_title) <= 5:
    #     article_title = soup.find("h1").text.replace("\n", " ").strip()

    # article_date = ""

    # We look for the first meta tag that has the word 'time' in it.
    # for item in soup.find_all("meta"):

    #     if "time" in item.get("property", ""):

    #         clean_date = item["content"].split("+")[0].replace("Z", "")
            
    #         # Use your preferred time formatting.
    #         article_date = "{:%d-%m-%Y a las %H:%M:%S}".format(
    #             datetime.fromisoformat(clean_date))
    #         break

    # If we didn't find any meta tag with a datetime we look for a 'time' tag.
    # if len(article_date) <= 5:
    #     try:
    #         article_date = soup.find("time").text.strip()
    #     except:
    #         pass

# def scrape_url(url):
#     nlp = spacy.load("en_core_web_sm")
#     url = clean_url(url)
#     url_content = scrape_content(url)
#     return url_content


# def scrape_content(urls):
#     clean_urls = []
#     content_list = []
#     for i in urls:
#         i = re.sub(r'.*url=',"",i)
#         i = re.sub(r'[&].*$',"",i)
#         # '+str(page) ***add to url for pagination***
#         clean_urls.append(i)

#     for v in clean_urls:
        # request = urlopen(v)
        # soup = BeautifulSoup(request, 'html.parser')
#         try:
#             title = None
#             link = None
#             author = None
#             time_published = None
#             content = soup.get_text("|", strip=True)
#             # content_list.append([content])
#             content_list.append([title, link, author, time_published, content])
#         except:
#             pass
#         # print(content_list)
#         sqlfile.receive_data(content_list)
    

# def scrapeUrl():
#     database = r"rss.db"
#     sql = """ select link from rss """   
#     urls = []
#     conn = sqlfile.create_connection(database) 
#     cur = conn.cursor()
#     cur.execute(sql)
#     rows = cur.fetchall()
#     for row in rows:
#         urls.append(row[0]) #maybe this should have ids or something like that in a dict instead to keep them in the right order once i've 'untupled?

#     return urls





    
    # return

    # print(urls)

    # return cur.lastrowid



    # print(soup.get_text())

    	# for v in url_list:
	# 	text = json.dumps(data["posts"][0]["link"], indent=2).strip('"')
			# printing as a json string with indentation level = 2
			# 
			# text = json.dumps(data, indent=2)
			# print(k)


			# link = re.sub(r'.*url=',"",text)
			# link = re.sub(r'[&].*$',"",link)

			# print(scrape.scrapeUrl(f'https://12ft.io/{link}'))
			# print(scrape.scrapeUrl(text))