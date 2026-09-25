# dcedl
Media downloader for [DiscordChatExporter](https://github.com/nulldg/DiscordChatExporter) JSON exports

## Building and installation
This project requires [uv](https://github.com/astral-sh/uv) to function.
```shell
# Clone the repo
git clone https://github.com/eldritchT/dcedl
cd dcedl
# Sync dependencies
uv sync # also add `--extra socks` if you want SOCKS proxies to work
# Build (wheels and tarballs are gonna end up in `./dist` directory)
uv build
# Install (preferably with `uv tool` but pipx and pip will do too)
uv tool install dist/*.whl
```

## Usage
```
usage: dcedl [-h] [-o OUTPUT] [--threads THREADS] [--overwrite] [-x PROXY] input

positional arguments:
  input                JSON file or directory of JSON files

options:
  -h, --help           show this help message and exit
  -o, --output OUTPUT  Output directory
  --threads THREADS    Maximum amount of parallel downloads
  --overwrite          Re-download and overwrite existing files
  -x, --proxy PROXY    Network proxy (SOCKS proxies require PySocks)
```

## How does it work
dcedl accepts a path to a JSON file or a directory with JSON files as `input` argument, extracts all URLs from the files and downloads them into the `OUTPUT` directory (defaults to `./downloads`), recreating the structure based on the URLs.
```
# Passing a directory with JSON files
user@theworldmachine ~ % dcedl ./dce --threads 4
[STRT] dcedl v0.2.0 by eldritchT
[WARN] ./dce/smth.json is not a DCE export, skipping
[INFO] Found 143 URLs

< truncated >

# Now let's look at the tree
user@theworldmachine ~ % cd downloads
user@theworldmachine ~/downloads % tree -L 2
.
├── cdn4.telesco.pe
│   └── file
├── cdn.discordapp.com
│   ├── attachments
│   ├── avatars
│   ├── emojis
│   ├── icons
│   └── stickers
├── cdn.jsdelivr.net
│   └── gh
├── images-ext-1.discordapp.net
│   └── external
├── i.ytimg.com
│   └── vi
├── media.discordapp.net
│   └── attachments
├── media.tenor.com
│   ├── 1eZIJHdfZGIAAAAe
│   └── zzvNuG5MDREAAAPo
├── shared.akamai.steamstatic.com
│   └── store_item_assets
├── shared.fastly.steamstatic.com
│   └── store_item_assets
├── static-cdn.jtvnw.net
│   └── twitch-video-assets
├── static.klipy.com
│   └── ii
└── upload.wikimedia.org
    └── wikipedia
```

## See also
- [nulldg/DiscordChatExporterPlus](https://github.com/nulldg/DiscordChatExporterPlus) - non-protestware fork of DCE
- [slatinsky/DiscordChatExporter-frontend](https://github.com/slatinsky/DiscordChatExporter-frontend) - convenient web-based viewer for DCE exports with a familiar Discord-like UI