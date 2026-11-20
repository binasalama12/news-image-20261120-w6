#!/usr/bin/env python3
"""Publisher for the w6 news-image entry (edition 20261120).

Design: "Numbers XL front page" — Friday 20 November 2026.
The finished artwork already lives in this repository as entry.png;
this small standard-library-only program validates that file and
copies it into the output directory the grader provides.
"""

import os
import shutil
import sys
from pathlib import Path

MAX_BYTES = 1048576  # competition cap: 1 MiB
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8\xff"
HEADLINE = "Numbers XL front page"
EDITION_DATE = "Friday 20 November 2026"


def find_artwork() -> Path:
    candidate = Path(__file__).resolve().parent / "entry.png"
    if not candidate.is_file():
        print(f"error: artwork not found at {candidate}", file=sys.stderr)
        raise SystemExit(1)
    return candidate


def validate(path: Path) -> int:
    size = path.stat().st_size
    with path.open("rb") as handle:
        head = handle.read(len(PNG_MAGIC))
    if not (head.startswith(PNG_MAGIC) or head.startswith(JPEG_MAGIC)):
        print("error: entry.png is neither PNG nor JPEG data", file=sys.stderr)
        raise SystemExit(1)
    if size > MAX_BYTES:
        print(f"error: entry.png is {size} bytes, over the {MAX_BYTES} cap",
              file=sys.stderr)
        raise SystemExit(1)
    return size


def publish(source: Path) -> Path:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    shutil.copyfile(source, target)
    return target


def main() -> int:
    artwork = find_artwork()
    size = validate(artwork)
    target = publish(artwork)
    print(f"{HEADLINE} - {EDITION_DATE}")
    print(f"done: published {size} bytes to {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
