from urllib.parse import urlparse, unquote, urlsplit
from pathlib import Path
import hashlib
import os

def truncate_filename(filename: str, max_length: int) -> str:
    name, ext = os.path.splitext(filename)
    if len(filename) <= max_length:
        return filename

    allowed_name_len = max_length - len(ext)
    if allowed_name_len <= 0:
        return filename[:max_length]

    return name[:allowed_name_len] + "..." + ext

def truncate_url(url, max_len=60):
    parts = urlsplit(url)
    host = parts.netloc
    filename = Path(parts.path).name

    if len(url) <= max_len:
        return url

    if filename:
        return f"{parts.scheme}://{host}/.../{truncate_filename(filename, 20)}"
    return f"{parts.scheme}://{host}/..."