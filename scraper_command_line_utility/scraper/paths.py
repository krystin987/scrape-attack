"""
Just a separate place to hold configured paths
"""
from datetime import datetime
import json
from pathlib import Path
import os

CACHE_DIR = Path.home() / ".cache" / "story_info"
CONFIG_DIR = Path.home() / ".config" / "story_info"
CACHED_STATIONINDEX = CACHE_DIR / "all-stations.json"

def get_cache_path(name):
    if CACHE_DIR.exists():
        print("Skipping")
    else:
        CACHE_DIR.mkdir(parents=True)
    parent = CACHE_DIR / "incoming_web_data_zips"
    os.makedirs(name, exist_ok=True)
    return parent / f"{name}_{datetime.now():%Y_%m_%d_%p}.zip"

def load_rss_config():
    if CONFIG_DIR.exists():
        print("Skipping")
    else:
        CONFIG_DIR.mkdir(parents=True)
    return json.load((CONFIG_DIR / "rss_feeds.json").open())

def load_whitelist():
    
    return (CONFIG_DIR / "whitelist.txt").read_text().splitlines()

def load_nopelist():
    return (CONFIG_DIR / "nopelist.txt").read_text().splitlines()

