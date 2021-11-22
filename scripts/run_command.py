import subprocess


def run(command: str, with_console: bool = True) -> None:
    output = subprocess.run(command.split(), capture_output=True, text=True)
    print()
    if with_console:
        print("```console")
        print(f"$ {command}")
    print(output.stdout.strip())
    if with_console:
        print("```")
    print()
