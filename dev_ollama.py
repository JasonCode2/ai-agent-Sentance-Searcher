import subprocess
import os
import sys

OLLAMA_PATH = os.path.join("ollama", "ollama.exe")


def run_ollama_command(args):
    try:
        process = subprocess.Popen(
            [OLLAMA_PATH] + args,
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr,
            text=True
        )
        process.wait()
    except FileNotFoundError:
        print("Error: ollama.exe not found in /ollama folder.")
    except Exception as e:
        print("Error running command:", e)


def main():
    print("=== Ollama Dev CLI ===")
    print("Type 'exit' to quit")
    print("Examples:")
    print("  list")
    print("  pull llama3")
    print("  run llama3")
    print()

    while True:
        user_input = input("ollama> ").strip()

        if user_input.lower() in ["exit", "quit"]:
            break

        if not user_input:
            continue

        args = user_input.split()
        run_ollama_command(args)


if __name__ == "__main__":
    main()