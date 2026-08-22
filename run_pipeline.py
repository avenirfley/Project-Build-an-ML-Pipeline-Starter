"""Launch the Hydra pipeline consistently on Windows, macOS, and Linux."""

import argparse
import shlex
import subprocess
import sys
from pathlib import Path


def parse_args():
    """Parse the parameters supplied by the MLflow project entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--steps", default="all")
    parser.add_argument("--hydra-options", nargs=argparse.REMAINDER, default=[])
    return parser.parse_args()


def parse_hydra_options(values):
    """Reassemble options that MLflow splits when launching on Windows."""
    options = " ".join(values).strip()
    if len(options) >= 2 and options[0] == options[-1] == '"':
        options = options[1:-1]
    return shlex.split(options) if options else []


def main():
    """Translate MLflow parameters into individual Hydra arguments."""
    args = parse_args()
    pipeline = Path(__file__).with_name("main.py")
    command = [
        sys.executable,
        str(pipeline),
        f'main.steps="{args.steps}"',
    ]
    command.extend(parse_hydra_options(args.hydra_options))
    subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
