import json
from pathlib import Path

CONFIG_FILE = Path.home() / "muget.json"

DEFAULT_CONFIG = {
    "audio_itag": "140",
    "output_directory": "YouTube Music",
    "delay_between_downloads": 1,
    "embed_cover": True,
    "cover_size": 1400,
    "cover_quality": 94,
    "save_cover": True, 
    "skip_existing": True,
    "cookies_path": None,
    "po_token": None,
    "replaygain": False,
    "use_aria2c": False,
    "log_level": "INFO"
}

def load_config():
    if not CONFIG_FILE.exists():

        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(
                DEFAULT_CONFIG,
                f,
                indent=4,
                ensure_ascii=False
            )

        print(f"[INFO] Configuration created: {CONFIG_FILE}")
        print()
        print("Review the configuration file before first use.")
        print("After editing it, run MuGet again.")

        raise SystemExit(0)

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = json.load(f)

    updated = False

    for key, value in DEFAULT_CONFIG.items():
        if key not in config:
            config[key] = value
            updated = True

    # NORMALIZACIÓN CORRECTA AQUÍ
    config["cookies_path"] = config.get("cookies_path") or None
    config["po_token"] = config.get("po_token") or None
    config["replaygain"] = config.get(
        "replaygain",
        False
    )

    if updated:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(
                config,
                f,
                indent=4,
                ensure_ascii=False
            )

        print("Configuration updated with new options")

    return config