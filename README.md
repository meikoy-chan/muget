# MuGet

Download music from YouTube Music.

## Features:

  * MuGet automatically embed metadata into audio file:

    - `title`
    - `artist`
    - `album`
    - `albumartist`
    - `track`
    - `totaltracks`
    - `date`
    - `cover art`
    - `lyrics` (when available)
    - `credits` (when available)
    
      ### Example:

        ```text
        Input #0, ogg, from '05 - Uma Thurman.opus':
        Duration: 00:03:31.58, start: 0.000000, bitrate: 147 kb/s
        Stream #0:0: Audio: opus, 48000 Hz, stereo, fltp
          Metadata:
            encoder         : Lavf63.3.100
            title           : Uma Thurman
            artist          : Fall Out Boy
            album_artist    : Fall Out Boy
            album           : American Beauty/American Psycho
            track           : 5
            tracktotal      : 11
            date            : 2015
            comment         : https://music.youtube.com/watch?v=r1AZQKsXKTY
            lyrics          : [00:00.08]I can move mountains
                            : [00:02.58]I can work a miracle, work a miracle
                            : [00:05.45]Oh, oh, keep you like an oath
                            : [00:09.24]May nothing but death do us part
                            : [00:13.43]♪
                            : [00:26.59]She wants to dance like Uma Thurman
                            : [00:29.11]Bury me till I confess
                            : [00:31.86]She wants to dance like Uma Thurman
                            : [00:35.37]And I can't get you out of my head
                            : [00:38.49]The stench, the stench, of summer sex
                            : [00:41.43]And CK eternity, oh hell yes
                            : [00:44.89]Divide me down to the smallest I can be
                            : [00:48.03]Put your, put your venom in me
                            : [00:51.33]I can move mountains
                            : [00:53.70]I can work a miracle, work a miracle
                            : [00:56.71]Oh, oh, I keep you like an oath
                            : [00:59.96]May nothing but death do us part
                            : [01:04.41]♪
                            : [01:16.93]She wants to dance like Uma Thurman
                            : [01:20.44]Bury me till I confess
                            : [01:23.09]She wants to dance like Uma Thurman
                            : [01:26.50]And I can't get you out of my head
                            : [01:29.47]The blood, the blood, the blood of the lamb
                            : [01:32.75]It's worth two lions, but here I am
                            : [01:35.81]And I slept in last night's clothes and tomorrow's dreams
                            : [01:40.06]But they're not quite what they seem
                            : [01:42.63]I can move mountains
                            : [01:44.90]I can work a miracle, work a miracle
                            : [01:47.91]Oh, oh, I keep you like an oath
                            : [01:51.09]May nothing but death do us part
                            : [01:55.66]♪
                            : [02:08.03]You'll find your way
                            : [02:10.62]And may death find you alive
                            : [02:13.98]Take me down the line
                            : [02:16.88]In Gem City we turn the tide
                            : [02:20.64]You'll find your way
                            : [02:23.29]And may death find you alive
                            : [02:27.37]Take me down the line
                            : [02:29.75]In Gem City we turn the tide
                            : [02:33.38]She wants to dance like Uma Thurman
                            : [02:37.05]Bury me till I confess
                            : [02:39.62]She wants to dance like Uma Thurman
                            : [02:43.08]And I can't get you out of my head
                            : [02:45.95]I can move mountains
                            : [02:48.69]I can work a miracle, work a miracle
                            : [02:52.08]Oh, oh, I keep you like an oath
                            : [02:54.87]May nothing but death do us part
                            : [02:59.52]I can move mountains
                            : [03:01.44]I can work a miracle, work a miracle
                            : [03:04.85]Oh, oh, I keep you like an oath
                            : [03:07.92]May nothing but death do us part
            performer       : Fall Out Boy
            composer        : Jake Sinclair; Andy Hurley; Pete Wentz; Joe Trohman; Waqaas Hashmi; Jarrel Young; Liam O'Donnell; Bob Mosher; Patrick Stump; Jack Marshall
            producer        : Jake Sinclair
            copyright       : Island Records
        Stream #0:1: Video: mjpeg (Baseline), yuvj420p(pc, bt470bg/unknown/unknown), 1400x1400 [SAR 1:1 DAR 1:1], 90k tbr, 90k tbn (attached pic)
            Metadata:
              comment         : Cover (front)
        ```

  * Downloaded files are organized automatically:

    ```text
    output_directory/
    └── Album Artist/
        └── Album/
            ├── 01 - Song.opus
            ├── 02 - Song.opus
            └── 03 - Song.opus
    ```

## Prequirements:

  * Before proceeding with the installation, make sure the following tools are installed and available in your PATH:

    - [Python](https://www.python.org)
    - [FFmpeg](https://www.ffmpeg.org)
    - [Deno](https://deno.com)
    - [Git](https://git-scm.com)

## Installation:

  * In your terminal type:

    ```bash
    pip install git+https://github.com/meikoy-chan/muget.git
    ```

## Configuration:

  The first time MuGet runs, it automatically creates a configuration file:

-   **Linux:**
      ```bash
      ~/muget.json
      ```
-   **Windows:**
      ```bash
      C:\Users\<username>\muget.json
      ```

    **Default configuration:**

    ```json
    {
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
    }
    ```
    > **Tip:** Edit this file to customize MuGet's behavior.

### Configuration Options

```text
Usage: muget [OPTIONS] [URL...]

  MuGet — YouTube Music Downloader.

  Downloads music from YouTube Music: songs, albums, and public playlists. Includes metadata,
  cover art, and optional ReplayGain support.

  CONFIGURATION:
    By default, settings are loaded from muget.json.
    Use -n to ignore the config file and use built-in defaults.
    Use --config-path to specify a different config file location.

  AUTHENTICATION (Premium):
    To download premium formats (itags 141, 774), provide:
      --cookies FILE    Netscape-format cookies file
      --po-token TOKEN  PoToken value

  EXAMPLES:
    muget "https://music.youtube.com/watch?v=..."
    muget -o ~/Music --audio-itag 251 "URL"
    muget --cookies cookies.txt --audio-itag 774 "URL"

Options:
  -v, --version                   Show the version and exit.
  --audio-itag ITAG               Audio quality itag
  -o, --output-dir DIR            Output directory for downloaded music
  --delay SECS                    Delay between downloads to avoid rate limiting
  --embed-cover / --no-embed-cover
                                  Embed cover art into audio files
  --cover-size PX                 Cover art resolution in pixels
  --cover-quality 1-100           Cover art JPEG quality (1-100)
  --save-cover / --no-save-cover  Save cover.jpg as separate file in album folder
  --skip-existing / --no-skip-existing
                                  Skip files that already exist
  --replaygain / --no-replaygain  Apply ReplayGain to albums (requires rsgain)
  --use-aria2c / --no-use-aria2c  Use aria2c for faster downloads
  --cookies FILE                  Netscape cookies file for YTM Premium formats
  --po-token TOKEN                PoToken for YTM Premium formats
  -l, --log-level [DEBUG|INFO]    Logging verbosity level
  --config-path FILE              Path to configuration file
  -n, --no-config-file            Ignore config file, use built-in defaults
  -h, --help                      Show this message and exit.
```

### Available Audio Formats

Available values for `audio_itag`:

|Itag|Quality|Codec|Container|Account|
|-|-|-|-|-|
|`249`|48kbps|opus|ogg|free|
|`250`|64kbps|opus|ogg|free|
|`251`|128kbps|opus|ogg|free|
|`774`|256kbps|opus|ogg|*premium*|
|`139`|48kbps|aac|m4a|free|
|`140`|128kbps|aac|m4a|free|
|`141`|256kbps|aac|m4a|*premium*|

> **Tip:** To download using the `774` or `141` itags, you must have an active YouTube Music Premium subscription and provide a valid *cookies_file*.

### Configuration Examples

**Specify a custom output directory:**

```json
"output_directory": "/home/user/Music"
```

**Download songs in Opus 128kbps (free):**

```json
"audio_itag": "251"
```

**Download songs in Opus 256kbps (premium):**

```json
"audio_itag": "774"
```

**Use browser cookies for authenticated downloads:**

```json
"cookies_path": "/home/user/cookies.txt"
```

## Usage

Run MuGet with the following command:

```bash
muget "URL"
```

**Supported URL types:**

- Song
- Album
- Public playlist

> **Tip:** Songs that are not "Official" (regular YouTube videos) are excluded by this program. To ensure you get valid links, use YouTube Music to search and enable the filter for songs or albums.

### Usage Examples

**Download a song:**

```bash
muget "https://music.youtube.com/watch?v=EfjIqEGHmDI"
```

**Download an album:**

```bash
muget "https://music.youtube.com/playlist?list=OLAK5uy_keZv-_VVAJ8GQ3gEx9c3a3araWrT0En0Y"
```

**Download a public playlist:**

```bash
muget "https://music.youtube.com/playlist?list=RDCLAK5uy_mzE-hKfgQBgAY_ZN4O85nOo_H9U0P47Mc"
```

## Acknowledgements

This project is based on [gytmdl](https://github.com/glomatico/gytmdl) and built on top of [ytmusicapi](https://github.com/sigma67/ytmusicapi). Thanks to the maintainers and contributors of both projects.