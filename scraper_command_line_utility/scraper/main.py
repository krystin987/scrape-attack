#! /usr/bin/env python3
import sys

from fetch_rss_data import fetch_urls, get_posts_details


def main():  # pylint: disable=inconsistent-return-statements
    """
    Example command-line utility
    """
    # pylint: disable=broad-except
    args = sys.argv[
           1:]  # By UNIX convention, sys.argv is a list of arguments, except the first one is the filename of this script
    for arg in args:
        posts = fetch_urls(arg)
        get_posts_details(posts, arg)
