#!/usr/bin/env python3
from __future__ import annotations

import argparse
import concurrent.futures as cf
from pathlib import Path
import json

from . import download, urlthings, utils

from rich.console import Console
csl = Console(highlight=False)

VERSION = "0.2.0"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path, help="JSON file or directory of JSON files")
    ap.add_argument("-o", "--output", type=Path, default=Path("downloads"), help="Output directory")
    ap.add_argument("--threads", type=int, default=8, help="Maximum amount of parallel downloads")
    ap.add_argument("--overwrite", action="store_true", help="Re-download and overwrite existing files")
    ap.add_argument("-x", "--proxy", type=str, default=None, help="Network proxy (SOCKS proxies require PySocks)")
    args = ap.parse_args()

    csl.print(f"[purple][STRT][/purple] [b]dcedl[/b] v{VERSION} by eldritchT")

    if args.proxy:
        if args.proxy.lower().startswith("socks"):
            try:
                import socks
            except ModuleNotFoundError:
                csl.print("[red][ERR][/red] SOCKS proxies require PySocks module to work")
                return
        download.SESSION.proxies = {
            "http": args.proxy,
            "https": args.proxy,
            "socks": args.proxy
        }

    urls = set()

    for jf in urlthings.iter_json_files(args.input):
        try:
            data = json.loads(jf.read_text(encoding="utf-8"))
            if not all([(x in data) for x in ['guild', 'channel']]):
                csl.print(f'[yellow][WARN][/yellow] {jf.name} is not a DCE export, skipping')
                continue
        except Exception:
            continue

        for u in urlthings.find_urls(data):
            if u.startswith(("http://", "https://")):
                urls.add(u)

    if not urls:
        csl.print("[cyan][INFO][/cyan] No URLs found")
        return

    csl.print(f"[cyan][INFO][/cyan] Found {len(urls)} URLs")

    ok = 0
    bad = 0
    with cf.ThreadPoolExecutor(max_workers=args.threads) as ex:
        futures = [ex.submit(download.download, u, args.output, args.overwrite) for u in sorted(urls)]
        try:
            for fut in cf.as_completed(futures):
                url, success, msg = fut.result()
                if success:
                    ok += 1
                else:
                    bad += 1
                msg_prefix = "[green][OKAY][/green]" if success else "[red][FAIL][/red]"
                csl.print(f"{msg_prefix} {utils.truncate_url(url, 40)} -> {msg}")
        except KeyboardInterrupt:
            csl.print("[cyan][INFO][/cyan] Interrupted by user")
            ex.shutdown(wait=False, cancel_futures=True)
            return

    csl.print(f"Done. ok={ok} bad={bad}")