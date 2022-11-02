import json
import os
from pathlib import Path
import tempfile
from zipfile import ZipFile

def walk_saved_entries(root):
    """
    For a directory root, produce an iterable of subdirectories, where each subdirectory has a metadata.json and
    content. Each entry is (subdirectory, dictionary of metadata, textual content).
    """
    root = Path(root)
    with tempfile.TemporaryDirectory() as td:
        ZipFile(root).extractall(td)
        for subdir, dirs, files in os.walk(td):
            subdir = Path(subdir)
            if "metadata.json" in files:
                content = (subdir / "content").read_text()
                metadata = json.load((subdir / "metadata.json").open())
                yield subdir, metadata, content