#!/usr/bin/env python3
"""Create one flat ZIP containing only validated, unique sticker media files."""

from __future__ import annotations

import argparse
import hashlib
import os
import sys
import tempfile
import zipfile
from pathlib import Path


SUPPORTED = {".gif", ".webp", ".png"}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def has_valid_signature(path: Path) -> bool:
    with path.open("rb") as stream:
        header = stream.read(12)

    suffix = path.suffix.lower()
    if suffix == ".gif":
        return header.startswith((b"GIF87a", b"GIF89a"))
    if suffix == ".png":
        return header.startswith(b"\x89PNG\r\n\x1a\n")
    if suffix == ".webp":
        return len(header) >= 12 and header[:4] == b"RIFF" and header[8:12] == b"WEBP"
    return False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate, exactly deduplicate, and package sticker media into one ZIP."
    )
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--force",
        action="store_true",
        help="replace the exact output ZIP if it already exists",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source = args.input.resolve()
    output = args.output.resolve()

    if not source.is_dir():
        raise SystemExit(f"error: input directory does not exist: {source}")
    if output.suffix.lower() != ".zip":
        raise SystemExit("error: output must use the .zip extension")
    if output.parent == source or source in output.parents:
        raise SystemExit("error: output ZIP must be outside the input directory")
    if output.exists() and output.is_dir():
        raise SystemExit(f"error: output path is a directory: {output}")
    if output.exists() and not args.force:
        raise SystemExit(f"error: output already exists; choose a new path or use --force: {output}")

    unique: list[Path] = []
    seen: set[str] = set()
    duplicate_count = 0
    invalid_count = 0

    for path in sorted(item for item in source.rglob("*") if item.is_file()):
        if path.suffix.lower() not in SUPPORTED:
            continue
        if not has_valid_signature(path):
            invalid_count += 1
            print(f"warning: skipped invalid {path.suffix.lower()} file: {path.name}", file=sys.stderr)
            continue
        key = digest(path)
        if key in seen:
            duplicate_count += 1
            continue
        seen.add(key)
        unique.append(path)

    if not unique:
        print("packaged=0")
        print(f"duplicates={duplicate_count}")
        print(f"invalid={invalid_count}")
        return 2

    output.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{output.stem}-", suffix=".tmp", dir=output.parent
    )
    os.close(descriptor)
    temporary = Path(temporary_name)

    try:
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for index, path in enumerate(unique, 1):
                archive.write(path, arcname=f"sticker-{index:03d}{path.suffix.lower()}")
        os.replace(temporary, output)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise

    formats = ",".join(sorted({path.suffix.lower().lstrip(".") for path in unique}))
    print(f"packaged={len(unique)}")
    print(f"duplicates={duplicate_count}")
    print(f"invalid={invalid_count}")
    print(f"formats={formats}")
    print(f"zip={output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
