"""
Python tests use pytest
"""
from pathlib import Path
from unittest.mock import patch

import pytest


# capsys is a special "fixture" parameter related to capturing standard output and standard error below
def test_main(capsys):
    from scraper.main import main  # The 'main' method is in a 'main' file
    # This is called Monkey patching. I replace sys.argv for anything running under "patch" here
    with patch("sys.argv", ["main",  # the first entry is the name of the script, which doesn't matter
                            "bow", "wow-wow-wow"]  # the rest are my chosen inputs
               ):
        # I call main, capturing its output
        main()
    captured = capsys.readouterr()
    assert captured.out == "Wicked cool arguments: ['bow', 'wow-wow-wow']\n"
