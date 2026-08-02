from urllib.parse import urlparse
from urllib.parse import parse_qs
import re

import unicodedata
from pathlib import Path

import colorama

import unicodedata

def resolve_input(url):

    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    if "v" in query:

        video_id = query["v"][0]

        return {
            "type": "song",
            "id": video_id
        }

    if "list" in query:

        list_id = query["list"][0]

        if list_id.startswith("OLAK"):

            return {
                "type": "album",
                "id": list_id
            }

        return {
            "type": "playlist",
            "id": list_id
        }

    raise ValueError(
        f"Unsupported URL: {url}"
    )


def force_best_cdn_cover(url: str, size: int, quality: int) -> str:    
    
    base = url.split('=')[0]
    base = re.sub(r'=(w|h|s)\d+.*$', '', base)
    return f"{base}=w{size}-l{quality}-rj"


def normalize_folder_name(name: str) -> str:

    return unicodedata.normalize(
        "NFKC",
        str(name)
    ).casefold()


def find_existing_folder(parent: Path, folder_name: str) -> Path:

    normalized_target = normalize_folder_name(folder_name)

    if parent.exists():

        for item in parent.iterdir():

            if not item.is_dir():
                continue

            if (
                normalize_folder_name(item.name)
                ==
                normalized_target
            ):
                return item

    return parent / folder_name
    
def color_text(text: str, color) -> str:

    return color + text + colorama.Style.RESET_ALL
        