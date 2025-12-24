"""
Cache functions
"""

from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

from platformdirs import user_cache_dir

CACHE_DIR = Path(user_cache_dir("pypistats"))


def filename(url: str) -> Path:
    """yyyy-mm-dd-url-slug.json"""
    from slugify import slugify

    today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    slug = slugify(url)
    return CACHE_DIR / f"{today}-{slug}.json"


def load(cache_file: Path):
    """Load data from cache_file"""
    if not cache_file.exists():
        return {}

    with cache_file.open("r") as f:
        try:
            data = json.load(f)
        except json.decoder.JSONDecodeError:
            return {}

    return data


def save(cache_file: Path, data) -> None:
    """Save data to cache_file"""
    try:
        if not CACHE_DIR.exists():
            CACHE_DIR.mkdir(parents=True)

        with cache_file.open("w") as f:
            json.dump(data, f)

    except OSError:
        pass


def clear() -> None:
    """Delete old cache files"""
    cache_files = CACHE_DIR.glob("**/*.json")
    this_month = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m")
    for cache_file in cache_files:
        if not cache_file.name.startswith(this_month):
            cache_file.unlink()
