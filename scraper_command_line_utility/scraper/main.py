#! /usr/bin/env python3
import sys

def main():  # pylint: disable=inconsistent-return-statements
    # pylint: disable=broad-except
    args = sys.argv[1:]  # By UNIX convention, sys.argv is a list of arguments, except the first one is the filename of this script
    print("Wicked cool arguments:", args)
