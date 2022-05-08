import requests
import sqlite3
from sqlite3 import Error
from bs4 import BeautifulSoup


def main():
    response = requests.get("https://www.nexstar.tv/stations/")
    if response.status_code != 200:
        print("Error fetching page")
        exit()
    else:
        content = response.content

    soup = BeautifulSoup(content, "html5lib")

    for link_tag in soup.find_all("a"):
        if link_tag.text.endswith(('.com')):
            print(link_tag.text)

    for markets in soup.find_all(attrs={'data-head': 'Market'}):
        market = markets.text
        market = " ".join(market.split())
        market = market.split(",")
        print(market)

    # tag = soup.td
    # attribute = tag.attrs
    # print(attribute)
    
    # web_site_domains = soup.find(data-head="Web Site")
    # print(web_site_domains)
#     response = requests.get('https://www.nexstar.tv/stations/')
#     soup = BeautifulSoup(response, "html5lib")

#     web_site_domains = soup.find_all('Web Site')
#     print(web_site_domains)


# 	# get_posts_details(posts)

main()