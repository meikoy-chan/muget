import json
import logging
from pathlib import Path

import click
import colorama

from . import __version__
from .downloader import YouTubeMusicDownloader
from .config import DEFAULT_CONFIG
from .utils import resolve_input
from .custom_logger import setup_logger

# Parameters that should not be saved to the config file
EXCLUDED_CONFIG_FILE_PARAMS = (
    "playlists",
    "config_path",
    "help",
    "version",
)


def write_default_config_file(config_path: Path) -> None:
    """Write the default configuration file if it doesn't exist."""
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        json.dumps(DEFAULT_CONFIG, indent=4, ensure_ascii=False)
    )


# Custom context settings for better help display
CONTEXT_SETTINGS = dict(
    help_option_names=["-h", "--help"],
    max_content_width=100,
)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.version_option(
    __version__,
    "-v",
    "--version",
    message="%(version)s",
)
# Main argument
@click.argument(
    "playlists",
    nargs=-1,
    type=str,
    required=True,
    metavar="URL [URL...]",
)
# Download options
@click.option(
    "--audio-itag",
    type=str,
    default=DEFAULT_CONFIG["audio_itag"],
    metavar="ITAG",
    help="Audio quality itag",
)
@click.option(
    "-o",
    "--output-dir",
    type=Path,
    default=Path(DEFAULT_CONFIG["output_directory"]),
    metavar="DIR",
    help="Output directory for downloaded music",
)
@click.option(
    "--delay",
    type=float,
    default=DEFAULT_CONFIG["delay_between_downloads"],
    metavar="SECS",
    help="Delay between downloads to avoid rate limiting",
)
# Cover art options
@click.option(
    "--embed-cover/--no-embed-cover",
    default=DEFAULT_CONFIG["embed_cover"],
    help="Embed cover art into audio files",
)
@click.option(
    "--cover-size",
    type=int,
    default=DEFAULT_CONFIG["cover_size"],
    metavar="PX",
    help="Cover art resolution in pixels",
)
@click.option(
    "--cover-quality",
    type=int,
    default=DEFAULT_CONFIG["cover_quality"],
    metavar="1-100",
    help="Cover art JPEG quality (1-100)",
)
@click.option(
    "--save-cover/--no-save-cover",
    default=DEFAULT_CONFIG["save_cover"],
    help="Save cover.jpg as separate file in album folder",
)
# Download behavior options
@click.option(
    "--skip-existing/--no-skip-existing",
    default=DEFAULT_CONFIG["skip_existing"],
    help="Skip files that already exist",
)
@click.option(
    "--replaygain/--no-replaygain",
    default=DEFAULT_CONFIG["replaygain"],
    help="Apply ReplayGain to albums (requires rsgain)",
)
@click.option(
    "--use-aria2c/--no-use-aria2c",
    default=DEFAULT_CONFIG["use_aria2c"],
    help="Use aria2c for faster downloads",
)
# Authentication options
@click.option(
    "--cookies",
    type=Path,
    default=Path(DEFAULT_CONFIG["cookies_path"]) if DEFAULT_CONFIG["cookies_path"] else None,
    metavar="FILE",
    help="Netscape cookies file for YTM Premium formats",
)
@click.option(
    "--po-token",
    type=str,
    default=DEFAULT_CONFIG["po_token"],
    metavar="TOKEN",
    help="PoToken for YTM Premium formats",
)
# Logging options
@click.option(
    "-l",
    "--log-level",
    type=click.Choice(["DEBUG", "INFO"]),
    default=DEFAULT_CONFIG["log_level"],
    help="Logging verbosity level",
)
# CLI configuration options
@click.option(
    "--config-path",
    type=Path,
    default=Path.home() / "muget.json",
    metavar="FILE",
    help="Path to configuration file",
)
@click.option(
    "-n",
    "--no-config-file",
    is_flag=True,
    default=False,
    help="Ignore config file, use built-in defaults",
)
def main(
    playlists: tuple[str, ...],
    audio_itag: str,
    output_dir: Path,
    delay: float,
    embed_cover: bool,
    cover_size: int,
    cover_quality: int,
    save_cover: bool,
    skip_existing: bool,
    cookies: Path | None,
    po_token: str | None,
    replaygain: bool,
    use_aria2c: bool,
    log_level: str,
    config_path: Path,
    no_config_file: bool,
) -> None:
    """
    MuGet — YouTube Music Downloader.

    Downloads music from YouTube Music: songs, albums, and public playlists.
    Includes metadata, cover art, and optional ReplayGain support.

    \b
    CONFIGURATION:
      By default, settings are loaded from muget.json.
      Use -n to ignore the config file and use built-in defaults.
      Use --config-path to specify a different config file location.

    \b
    AUTHENTICATION (Premium):
      To download premium formats (itags 141, 774), provide:
        --cookies FILE    Netscape-format cookies file
        --po-token TOKEN  PoToken value

    \b
    EXAMPLES:
      muget "https://music.youtube.com/watch?v=..."
      muget -o ~/Music --audio-itag 251 "URL"
      muget --cookies cookies.txt --audio-itag 774 "URL"
    """
    
    colorama.just_fix_windows_console()
    logger = setup_logger(level=log_level)
    
    if no_config_file:
        logger.debug("Using default config")
        
        audio_itag = str(DEFAULT_CONFIG["audio_itag"])
        output_dir = Path(DEFAULT_CONFIG["output_directory"])
        delay = float(DEFAULT_CONFIG["delay_between_downloads"])
        embed_cover = bool(DEFAULT_CONFIG["embed_cover"])
        cover_size = int(DEFAULT_CONFIG["cover_size"])
        cover_quality = int(DEFAULT_CONFIG["cover_quality"])
        save_cover = bool(DEFAULT_CONFIG["save_cover"])
        skip_existing = bool(DEFAULT_CONFIG["skip_existing"])
        replaygain = bool(DEFAULT_CONFIG["replaygain"])
        use_aria2c = bool(DEFAULT_CONFIG["use_aria2c"])
        log_level = DEFAULT_CONFIG["log_level"]
        cookies = Path(DEFAULT_CONFIG["cookies_path"]) if DEFAULT_CONFIG["cookies_path"] else None
        po_token = DEFAULT_CONFIG["po_token"] or None
        
    else:
        # Create config file if it doesn't exist
        if not config_path.exists():
            write_default_config_file(config_path)
            click.echo(f"Configuration file created: {config_path}")
            click.echo("Review the configuration file before first use.")
            click.echo("After editing it, run MuGet again.")
            raise SystemExit(0)
        
        # Detect if any CLI flags were passed
        ctx = click.get_current_context()
        any_cli_flag = False
        
        exclude_from_check = {"playlists", "config_path", "no_config_file", "help", "version"}
        
        for param in ctx.command.params:
            param_name = param.name
            if param_name in exclude_from_check:
                continue
            source = ctx.get_parameter_source(param_name)
            if source == click.core.ParameterSource.COMMANDLINE:
                any_cli_flag = True
                break
        
        # No flags passed, load from config file
        if not any_cli_flag:
            config_file = json.loads(config_path.read_text())
            
            audio_itag = str(config_file.get("audio_itag", DEFAULT_CONFIG["audio_itag"]))
            output_dir = Path(config_file.get("output_directory", DEFAULT_CONFIG["output_directory"]))
            delay = float(config_file.get("delay_between_downloads", DEFAULT_CONFIG["delay_between_downloads"]))
            embed_cover = bool(config_file.get("embed_cover", DEFAULT_CONFIG["embed_cover"]))
            cover_size = int(config_file.get("cover_size", DEFAULT_CONFIG["cover_size"]))
            cover_quality = int(config_file.get("cover_quality", DEFAULT_CONFIG["cover_quality"]))
            save_cover = bool(config_file.get("save_cover", DEFAULT_CONFIG["save_cover"]))
            skip_existing = bool(config_file.get("skip_existing", DEFAULT_CONFIG["skip_existing"]))
            replaygain = bool(config_file.get("replaygain", DEFAULT_CONFIG["replaygain"]))
            use_aria2c = bool(config_file.get("use_aria2c", DEFAULT_CONFIG["use_aria2c"]))
            log_level = config_file.get("log_level", DEFAULT_CONFIG["log_level"])
            
            cookies_path = config_file.get("cookies_path")
            cookies = Path(cookies_path) if cookies_path else None
            
            po_token = config_file.get("po_token") or None
            
            logger = setup_logger(level=log_level)
            logger.debug("No flags detected, using muget.json configuration")
    
    # Build configuration dictionary from parameters
    config = {
        "audio_itag": audio_itag,
        "output_directory": str(output_dir),
        "delay_between_downloads": delay,
        "embed_cover": embed_cover,
        "cover_size": cover_size,
        "cover_quality": cover_quality,
        "save_cover": save_cover,
        "skip_existing": skip_existing,
        "cookies_path": str(cookies) if cookies else None,
        "po_token": po_token,
        "replaygain": replaygain,
        "use_aria2c": use_aria2c,
        "log_level": log_level,
    }
    
    logger.info("Starting MuGet")

    for i, playlist in enumerate(playlists):
        is_last = (i == len(playlists) - 1)
        logger.info(f"URL {i+1}/{len(playlists)}: {playlist}") 
        logger.info("Fetching URL info... Please wait, this may take a while.")

        # Parse the playlist URL or ID
        input_info = resolve_input(playlist)

        # Initialize and run the downloader
        downloader = YouTubeMusicDownloader(
            input_info,
            config,
            output_dir=config["output_directory"],
        )

        downloader.run(cleanup=is_last)