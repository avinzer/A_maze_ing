import os
import sys

from mazegen.Renderer import interactive_loop, make_generator
from utils.parse_arges import parse_args, validate_config

os.system("cls" if os.name == "nt" else "clear")


def main() -> None:
    config = parse_args(sys.argv[1])
    validated_data = validate_config(config)
    gen = make_generator(validated_data)

    interactive_loop(validated_data, gen)


main()
