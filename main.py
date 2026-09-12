"""A safe, simple command-line folder organizer."""

from __future__ import annotations

import argparse
import shutil
import sys
from collections import Counter
from pathlib import Path


CATEGORIES: dict[str, str] = {
    # Images
    ".avif": "Images", ".bmp": "Images", ".gif": "Images", ".heic": "Images",
    ".jpeg": "Images", ".jpg": "Images", ".png": "Images", ".svg": "Images",
    ".tiff": "Images", ".webp": "Images",
    # Documents
    ".csv": "Documents", ".doc": "Documents", ".docx": "Documents", ".epub": "Documents",
    ".md": "Documents", ".ods": "Documents", ".odt": "Documents", ".pdf": "Documents",
    ".ppt": "Documents", ".pptx": "Documents", ".rtf": "Documents", ".txt": "Documents",
    ".xls": "Documents", ".xlsx": "Documents",
    # Audio / video
    ".aac": "Music", ".flac": "Music", ".m4a": "Music", ".mp3": "Music",
    ".ogg": "Music", ".wav": "Music",
    ".avi": "Videos", ".mkv": "Videos", ".mov": "Videos", ".mp4": "Videos",
    ".mpeg": "Videos", ".mpg": "Videos", ".webm": "Videos",
    # Archives
    ".7z": "Compressed", ".gz": "Compressed", ".rar": "Compressed", ".tar": "Compressed",
    ".zip": "Compressed",
    # Code
    ".c": "Code", ".cpp": "Code", ".cs": "Code", ".css": "Code", ".dart": "Code",
    ".go": "Code", ".html": "Code", ".java": "Code", ".js": "Code", ".json": "Code",
    ".php": "Code", ".py": "Code", ".rs": "Code", ".ts": "Code", ".tsx": "Code",
}


def unique_destination(destination: Path) -> Path:
    """Return an unused destination without overwriting an existing file."""
    if not destination.exists():
        return destination

    number = 1
    while True:
        candidate = destination.with_name(
            f"{destination.stem} ({number}){destination.suffix}"
        )
        if not candidate.exists():
            return candidate
        number += 1


def organize(folder: Path, dry_run: bool = False) -> Counter[str]:
    """Sort files directly inside *folder* and return the counts by category."""
    counts: Counter[str] = Counter()

    for item in folder.iterdir():
        if not item.is_file() or item.name.startswith("."):
            continue

        category = CATEGORIES.get(item.suffix.lower(), "Other")
        destination = unique_destination(folder / category / item.name)

        if dry_run:
            print(f"  {item.name}  ->  {category}/{destination.name}")
        else:
            destination.parent.mkdir(exist_ok=True)
            shutil.move(str(item), str(destination))

        counts[category] += 1

    return counts


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sort files in a folder into category folders.",
        epilog="Example: python main.py C:/Users/you/Downloads --dry-run",
    )
    parser.add_argument("folder", nargs="?", help="Folder to organize")
    parser.add_argument(
        "--dry-run", action="store_true", help="Preview changes without moving files"
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    folder_input = args.folder or input("Folder path to organize: ").strip().strip('"')
    folder = Path(folder_input).expanduser()

    if not folder.is_dir():
        print(f"Error: '{folder}' is not a valid folder.", file=sys.stderr)
        return 1

    action = "Previewing" if args.dry_run else "Organizing"
    print(f"{action}: {folder}\n")
    counts = organize(folder, args.dry_run)

    if not counts:
        print("No files to organize.")
        return 0

    total = sum(counts.values())
    print(f"\n{'Would organize' if args.dry_run else 'Organized'} {total} file(s):")
    for category, count in sorted(counts.items()):
        print(f"  - {category}: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
