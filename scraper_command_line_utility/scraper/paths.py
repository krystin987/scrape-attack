"""
Just a separate place to hold configured paths
"""
from pathlib import Path

CACHE_DIR = Path.home() / ".cache" / "butts"
CONFIG_DIR = Path.home() / ".config" / "butts"
CACHED_STATIONINDEX = CACHE_DIR / "all-stations.json"

def load_whitelist():
    return (CONFIG_DIR / "whitelist.txt").read_text().splitlines()

