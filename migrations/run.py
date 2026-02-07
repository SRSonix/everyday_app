import subprocess
import sys


def main() -> None:
    args = sys.argv[1:] if len(sys.argv) > 1 else ["upgrade", "head"]
    subprocess.run(["alembic", *args], check=True)


if __name__ == "__main__":
    main()
