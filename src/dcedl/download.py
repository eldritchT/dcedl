from urllib.parse import urlparse, unquote
from rich import get_console
from pathlib import Path
import hashlib
import math
import os

from .utils import truncate_filename

import requests

SESSION = requests.Session()
SESSION.headers.update(
    {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0",
        "Accept": "*/*",
    }
)

def url_to_output_path(url: str, out_root: Path) -> Path:
    p = urlparse(url)
    host = p.netloc.lower()
    path = unquote(p.path).lstrip("/")

    # Preserve URL structure under host
    rel = Path(host) / Path(path)

    # Keep querystring uniqueness when needed (e.g. Discord CDN format params)
    if p.query:
        stem = rel.name
        suffix = rel.suffix
        qhash = hashlib.sha1(p.query.encode("utf-8")).hexdigest()[:10]
        if suffix:
            rel = rel.with_name(f"{stem[: max(1, len(stem) - len(suffix))]}_{qhash}{suffix}")
        else:
            rel = rel / qhash

    return out_root / rel

def download(url: str, out_root: Path, overwrite: bool = False) -> tuple[str, bool, str]:
    try:
        dst = url_to_output_path(url, out_root)
        dst.parent.mkdir(parents=True, exist_ok=True)

        if dst.exists() and not overwrite:
            return url, True, "exists"

        try:
            with SESSION.get(url, stream=True, timeout=30) as r:
                r.raise_for_status()
                tmp = dst.with_suffix(dst.suffix + ".part")
                with open(tmp, "wb") as f:
                    content_length = r.headers.get('Content-Length')
                    chunk_size = 1024 * 256
                    total = math.ceil(int(content_length) / chunk_size) if content_length else 0
                    short_name = truncate_filename(dst.name, 40)
                    with get_console().status(f"{short_name}") as st:
                        downloaded_chunks = 0
                        for chunk in r.iter_content(chunk_size=chunk_size):
                            if chunk:
                                st.update(f"{short_name} [{downloaded_chunks}/{total} chunks] ")
                                f.write(chunk)
                                downloaded_chunks += 1
                        st.stop()
                os.replace(tmp, dst)
            return url, True, "downloaded"
        except Exception as e:
            msg = str(e)
            match r.status_code:
                case 401:
                    msg = "bad request"
                case 403:
                    msg = "forbidden"
                case 404:
                    msg = "not found"
                case _:
                    if str(r.status_code).startswith("5"):
                        msg = f"server error ({r.status_code})"
            return url, False, msg
    except KeyboardInterrupt:
        return url, False, "kbd interrupt"