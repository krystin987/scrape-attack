import requests
import sqlite3
from sqlite3 import Error
from bs4 import BeautifulSoup
from scrape import clean_url
# import re
HEADERS = {"User-Agent": "Summarizer v2.0"}


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.execute("CREATE TABLE IF NOT EXISTS station (callsign, id, city, state)") # , web_site, programming, station_info, channels, market
    except Error as e:
        print(e)

    return conn

def insert_station_data(conn, station_list):
    sql = """ insert into station values (?, ?, ?, ?) """ #, ?, ?, ?, ?, ?, ?, ?
    cur = conn.cursor()
    cur.executemany(sql, station_list)
    conn.commit()

def receive_data(data):
    database = r"station.db"
    conn = create_connection(database)
    insert_station_data(conn, data)

def scrape_station_info(link):
    try: 
        with requests.get(link, headers=HEADERS, timeout=10) as response:
            text = response.text.lower()
            soup = BeautifulSoup(text, "html5lib")
            # soup = soup.find(attrs={"class": "site-center"})
            for tag in soup.find_all(["p", "a", "font"]):
                try:
                    callsign = link.replace("https://www.stationindex.com/tv/callsign/", "").lower()
                    if tag.text.startswith("id"):
                        id = tag.text.replace("id:", tag.next_element.next_element.strip())
                    if tag.text.startswith("city"):
                        city = tag.text.replace("city: ", "").split(",")[0]
                        state = tag.text.replace("city: ", "").split(",")[1]
                    # if tag.text.startswith("web site"):
                    #     web_site = tag.text.replace("web site: ", "")
                    # if tag.text.startswith("programming"):
                    #     programming = tag.text.replace("programming :", "")
                    # if tag.text.startswith("station info"):
                    #     station_info = tag.text.replace("station info: ", "")
                    # if tag.text.startswith("channels"):
                    #     channels = tag.text.replace("channels:", "")
                    # if tag.text.startswith("market"):
                    #     market = tag.text.replace("market: ", "")
                    return(callsign, id, city, state) #, web_site, programming, station_info, channels, market
                    
                except:
                    pass                  
    except:
        return("error") 

def get_station_info(links):
    link_data = []
    for link in links:
        try: 
            with requests.get(link, headers=HEADERS, timeout=10) as response:
                content = response.content
                soup = BeautifulSoup(content, "html5lib")
                for callsign_link in soup.find_all(href=True):
                    link = callsign_link.get("href")
                    if link.startswith(("https://www.stationindex.com/tv/callsign/")):
                        data = scrape_station_info(link)
                        print(data)
                        link_data.append(data)

        except:
            return("error")
    print(len(link_data))
    receive_data(link_data)
        


def main():
    response = requests.get("https://www.stationindex.com/tv/by-owner")
    if response.status_code != 200:
        print("Error fetching page")
        exit()
    else:
        content = response.content

    soup = BeautifulSoup(content, "html5lib")
    station_links = []
    for link_tag in soup.find_all(href=True):
        link = link_tag.get("href")
        if link.startswith(("/tv/by-owner/")):
            station_links.append("https://www.stationindex.com" + link)
    get_station_info(station_links)


main()