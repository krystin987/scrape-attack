#! /usr/bin/env python3
import json
from pathlib import Path

import click
import requests
from rich import progress
from rich.console import Console
from rich.table import Table

from . import client

table_args = {"show_edge": False}


@click.group()
@click.pass_context
def cli(ctx):
    # assert not ctx.invoked_subcommand
    pass


@cli.command("dump")
@click.option("--refresh/--cached", help="Download pages again")
@click.argument("path", type=Path)
def cli_dump(path, refresh):
    """
    Produce a JSON of stations by owner
    """
    structured_stations_by_owner = {}
    with requests.Session() as session:
        for name, link in progress.track(client.get_station_owners(refresh=refresh).items()):
            structured_stations_by_owner[name] = client.get_stations_by_owner(name, refresh=refresh, session=session)
    json.dump(structured_stations_by_owner, path.open("w"), indent=2, default=str)


@cli.command("show")
@click.argument("path", type=Path)
def cli_show(path):
    """
    Using a cached JSON file, show all stations with web pages
    """
    table = Table("owner", "name", "web site", **table_args)
    for owner, stations in json.load(path.open()).items():
        for name, station in stations.items():
            if "callsign" in station:
                callsign, link, info = station["callsign"]
                if "Web Site" in info:
                    table.add_row(owner, name, info["Web Site"])
    Console().print(table)


def main():  # pylint: disable=inconsistent-return-statements
    # pylint: disable=broad-except
    try:
        cli(obj={})  # pylint: disable=no-value-for-parameter,unexpected-keyword-arg
    except Exception as e:
        print(e)
        return e
