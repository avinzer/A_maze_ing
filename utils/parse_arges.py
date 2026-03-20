import sys
from typing import Dict, List, Optional, Tuple

_REQUIRED_KEYS: List[str] = [
    "WIDTH",
    "HEIGHT",
    "ENTRY",
    "EXIT",
    "OUTPUT_FILE",
    "PERFECT",
]


def _die(message: str) -> None:
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


def parse_args(config_file: str) -> Dict[str, str]:
    config_data: Dict[str, str] = {}
    try:
        with open(config_file, "r") as file:
            for line_num, data in enumerate(file):
                line = data.strip()

                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    _die(
                        f"Confige line {line_num}: "
                        f"expected Key=Value, got: {line!r}"
                    )
                key, _, value = line.partition("=")
                config_data[key.strip().upper()] = value.strip()

    except FileNotFoundError:
        _die(f"Config file not found: {config_file!r}")
    except OSError as exc:
        _die(f"Cannot read config file: {exc}")

    return config_data


def validate_config(config: Dict[str, str]) -> Dict:
    for key in _REQUIRED_KEYS:
        if key not in config:
            _die(f"Missing required config key: {key}")
    try:
        width: int = int(config["WIDTH"])
        height: int = int(config["HEIGHT"])
        if width < 2 or height < 2:
            raise ValueError("WIDTH and HEIGHT must each be at least 2")
        e_parts = config["ENTRY"].split(",")
        x_parts = config["EXIT"].split(",")
        if len(e_parts) != 2 or len(x_parts) != 2:
            raise ValueError("ENTRY and EXIT must be two pair: (x, y)")
        entry: Tuple[int, int] = (
            int(e_parts[0].strip()), int(e_parts[1].strip()))
        exit_: Tuple[int, int] = (
            int(x_parts[0].strip()), int(x_parts[1].strip()))

        if not (0 <= entry[0] < width and 0 <= entry[1] < height):
            raise ValueError(
                f"ENTRY {entry} is outside the maze bounds ({width}x{height})."
            )
        if not (0 <= exit_[0] < width and 0 <= exit_[1] < height):
            raise ValueError(
                f"EXIT {exit_} is outside the maze bounds ({width}x{height})."
            )
        if entry == exit_:
            raise ValueError("ENTRY and EXIT must be different cells.")

        perfect_str = config["PERFECT"].strip().lower()
        if perfect_str not in ("true", "false"):
            raise ValueError("PERFECT must be 'True' or 'False'.")
        perfect = perfect_str == "true"

        seed: Optional[int] = None
        if "SEED" in config:
            seed = int(config["SEED"])

        animation: Optional[bool] = False
        if "ANIMATION" in config:
            if config["ANIMATION"] == "True":
                animation = True

        output_file = config["OUTPUT_FILE"].strip()
        if not output_file:
            raise ValueError("OUTPUT_FILE must not be empty.")

    except ValueError as exc:
        _die(f"Invalid configuration value: {exc}")

    return {
        "width": width,
        "height": height,
        "entry": entry,
        "exit_": exit_,
        "output_file": output_file,
        "perfect": perfect,
        "seed": seed,
        "animation": animation
    }
