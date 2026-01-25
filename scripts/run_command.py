from __future__ import annotations

import os
import subprocess


def run(command: str, with_console: bool = True) -> None:
    # Use a fixed terminal width for consistent output
    env = os.environ.copy()
    env["COLUMNS"] = "88"
    output = subprocess.run(command.split(), capture_output=True, text=True, env=env)
    print()
    if with_console:
        print("```console")
        print(f"$ {command}")
    print(output.stdout.strip())
    if with_console:
        print("```")
    print()
