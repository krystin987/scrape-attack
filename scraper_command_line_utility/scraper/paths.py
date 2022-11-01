"""
Just a separate place to hold configured paths
"""
from datetime import datetime
import json
from pathlib import Path
import os

CACHE_DIR = Path.home() / ".cache" / "butts"
CONFIG_DIR = Path.home() / ".config" / "butts"
CACHED_STATIONINDEX = CACHE_DIR / "all-stations.json"

def get_cache_path(name):
    parent = CACHE_DIR / "incoming_web_data_zips"
    os.makedirs(name, exist_ok=True)
    return parent / f"{name}_{datetime.now():%Y_%m_%d_%p}.zip"

def load_rss_config():
    return json.load((CONFIG_DIR / "rss_feeds.json").open())

def load_whitelist():
    return (CONFIG_DIR / "whitelist.txt").read_text().splitlines()

