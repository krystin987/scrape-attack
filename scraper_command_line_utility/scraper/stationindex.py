import json
import sqlite3

import tldextract

from .paths import *

def read_stationindex(path=CACHED_STATIONINDEX):
    db_list = []
    with open(path) as f:
        station_data = json.load(f)
    for owner, stations_by_id in station_data.items():
        for station_id, info in stations_by_id.items():
            callsign, _, callsign_info = info["callsign"]
            # Mebbe the API could do this change
            lowercase_callsign_info = {
                k.lower().replace(" ", "_"): v for k, v in callsign_info.items()
            }

            city = lowercase_callsign_info['city']
            # state = lowercase_callsign_info['city'].split(",")[1]
            web_site = lowercase_callsign_info.get('web_site')
            if web_site:
                ext = tldextract.extract(web_site)
                domain = "{}.{}".format(ext.domain, ext.suffix)
            programming = lowercase_callsign_info['programming']
            station_info = lowercase_callsign_info['station_info']
            channels = lowercase_callsign_info.get('channels')
            market = lowercase_callsign_info.get('market')
            db_list.append([callsign, station_id, city, web_site, domain, programming, station_info, channels, market])
    return db_list


def import_stations(rows):
    database = r"station.db"
    conn = sqlite3.connect(database)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS station (callsign, station_id, city, web_site, domain, programming, station_info, channels, market)")
    sql = """ insert into station values (?, ?, ?, ?, ?, ?, ?, ?, ?) """
    cur = conn.cursor()
    cur.executemany(sql, rows)
    conn.commit()