#!/usr/bin/env python

import os.path
import sys
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("--json", action="store_true", help="Enable structured JSON output")
args, unknown = parser.parse_known_args()
use_json = args.json

def print_json(obj):
    print(json.dumps(obj))

try:
    from core.cli.main import run_pythagora
except ImportError as err:
    pythagora_root = os.path.dirname(__file__)
    venv_path = os.path.join(pythagora_root, "venv")
    requirements_path = os.path.join(pythagora_root, "requirements.txt")
    if sys.prefix == sys.base_prefix:
        venv_python_path = os.path.join(venv_path, "scripts" if sys.platform == "win32" else "bin", "python")
        msg = f"Python environment for Pythagora is not set up: module `{err.name}` is missing."
        if use_json:
            print_json({"error": msg})
        else:
            print(msg, file=sys.stderr)
            print(f"Please create Python virtual environment: {sys.executable} -m venv {venv_path}", file=sys.stderr)
            print(f"Then install dependencies with: {venv_python_path} -m pip install -r {requirements_path}", file=sys.stderr)
    else:
        msg = f"Python environment for Pythagora is not completely set up: module `{err.name}` is missing"
        if use_json:
            print_json({"error": msg})
        else:
            print(msg, file=sys.stderr)
            print(f"Please run `{sys.executable} -m pip install -r {requirements_path}` to finish setup.", file=sys.stderr)
    sys.exit(255)

if use_json:
    print_json({"status": "starting", "message": "Launching GPT-Pilot in JSON mode"})

exit_code = run_pythagora()

if use_json:
    print_json({"status": "done", "exit_code": exit_code})
else:
    print("Pythagora finished.")

sys.exit(exit_code)

