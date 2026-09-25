from pathlib import Path
import re

URL_RE = re.compile(r"https?://[^\s<>'\"()]+")

def iter_json_files(path: Path):
    if path.is_file():
        yield path
    else:
        yield from path.rglob("*.json")

def find_urls(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str):
                if k.lower() in {"url", "avatarurl", "attachmenturl", "thumbnailurl", "imageurl"}:
                    yield v
                else:
                    yield from URL_RE.findall(v)
            else:
                yield from find_urls(v)
    elif isinstance(obj, list):
        for item in obj:
            yield from find_urls(item)
    elif isinstance(obj, str):
        yield from URL_RE.findall(obj)