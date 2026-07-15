# MuGet

Download YouTube Music audio with metadata.

## Requirements

Before using MuGet, make sure the following tools are installed and available in your PATH:

* [Python](https://www.python.org)
* [FFmpeg](https://www.ffmpeg.org)
* [Deno](https://deno.com)
* [Git](https://git-scm.com)

## Installation

In your terminal type:

```bash
pip install git+https://github.com/meikoy-chan/muget.git
```

## Configuration

The first time MuGet runs, it automatically creates a configuration file:

• Linux: 
```bash
~/muget.json
```
• Windows: 
```bash
C:\Users\<username>\muget.json
```

**Default configuration:**

```json
    "audio_itag": "140",
    "output_directory": "YouTube Music",
    "delay_between_downloads": 1,
    "embed_cover": true,
    "cover_size": 1400,
    "cover_quality": 90,
    "save_cover": false,
    "skip_existing": true,
    "cookies_path": null,
    "po_token": null,
    "replaygain": false,
    "use_aria2c": false,
    "log_level": "INFO"
```
> **Tip:** Edit this file to customize MuGet's behavior.

* **Configuration Options:**

```text
Usage: muget [OPTIONS] URL [URL...]

  MuGet - YouTube Music Playlist Downloader.

  Downloads music from YouTube Music playlists, albums, or individual songs
  with metadata, cover art, and optional ReplayGain support.

  Configuration is loaded from muget.json when no flags are passed. Any flag
  passed will use its default value instead of the config file.

Options:
  -h, --help                      Show this message and exit.
  -v, --version                   Show the version and exit.
  --audio-itag TEXT               Audio quality itag (e.g., 140 for AAC, 251
                                  for Opus)
  -o, --output-dir PATH           Directory where downloaded music will be
                                  saved
  --delay FLOAT                   Delay in seconds between downloads to avoid
                                  rate limiting
  --embed-cover / --no-embed-cover
                                  Embed cover art into audio files
  --cover-size INTEGER            Cover art resolution in pixels
  --cover-quality INTEGER         Cover art JPEG quality (1-100)
  --save-cover / --no-save-cover  Save cover.jpg as a separate file in the
                                  album folder
  --skip-existing / --no-skip-existing
                                  Skip downloading files that already exist
  --replaygain / --no-replaygain  Calculate and apply ReplayGain to albums
                                  (requires rsgain)
  --use-aria2c / --no-use-aria2c  Use aria2c as the external downloader for
                                  faster downloads
  --cookies PATH                  Path to Netscape format cookies file for
                                  YouTube Music Premium formants
  --po-token TEXT                 PoToken for YouTube Music Premium formats
  -l, --log-level [DEBUG|INFO]    Set the logging verbosity level
  --config-path PATH              Path to the configuration file
  -n, --no-config-file            Ignore the config file and use only command-
                                  line arguments
```

* **Available Audio Formats:**

Available values for `audio_itag`:

|Itag|Quality|Codec|Container|Account|
|-|-|-|-|-|
|`249`|`48kbps`|`opus`|`ogg`|`free`|
|`250`|`64kbps`|`opus`|`ogg`|`free`|
|`251`|`128kbps`|`opus`|`ogg`|`free`|
|`774`|`256kbps`|`opus`|`ogg`|`premium`|
|`139`|`48kbps`|`aac`|`m4a`|`free`|
|`140`|`128kbps`|`aac`|`m4a`|`free`|
|`141`|`256kbps`|`aac`|`m4a`|`premium`|
> **Tip:** To download using the `774` or `141` itags, you must have an active YouTube Music Premium subscription and provide `Cookies_File`.

## **Examples:**

Specify a custom `output directory`:

```json
"output_directory": "/home/user/Music"
```

Download format Ogg/Opus:

```json
"audio_itag": "`251`"
```

Use browser cookies for authenticated downloads:

```json
"cookies_path": "/home/user/cookies.txt"
```

## Usage

Run MuGet with the following command:

```bash
muget "YOUR_URL"
```

• Supported URL types:

* `Song`
* `Album`
* `Public playlist`

>**Tip.** **Songs that are not "Official" (regular YouTube videos) are excluded by this program.** To ensure you get valid links, use YouTube Music to search and enable the filter for songs or albums.

* **Examples:**

* **Download a song:**
  ```bash
    muget https://music.youtube.com/watch?v=EfjIqEGHmDI
  ```
* **Download an album:**
  ```bash
    muget https://music.youtube.com/playlist?list=OLAK5uy_keZv-_VVAJ8GQ3gEx9c3a3araWrT0En0Y
  ```
* **Download a public playlist:**
  ```bash
    muget https://music.youtube.com/playlist?list=RDCLAK5uy_mzE-hKfgQBgAY_ZN4O85nOo_H9U0P47Mc
  ```
  
## Output

Downloaded files are organized automatically:

```text
output_directory/
└── Album Artist/
    └── Album/
        ├── 01 - Song.opus
        ├── 02 - Song.opus
        └── 03 - Song.opus
```

## Metadata

MuGet automatically writes:

* `title`
* `artist`
* `album`
* `albumartist`
* `track`
* `totaltracks`
* `date`
* `cover art`
* `lyrics (when available)`
* `credits (when available)`

## Acknowledgements

This project is based on [gytmdl](https://github.com/glomatico/gytmdl) and built on top of [ytmusicapi](https://github.com/sigma67/ytmusicapi). Thanks to the maintainers and contributors of both projects.

