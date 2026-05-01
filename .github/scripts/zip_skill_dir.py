#!/usr/bin/env python3
"""
Create a zip file for a skill directory.
"""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path


def zip_skill_dir(skills_dir: Path, zip_name: str) -> Path:
    zip_path = skills_dir / zip_name
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in skills_dir.rglob("*"):
            if path == zip_path or path.is_dir():
                continue
            rel_path = path.relative_to(skills_dir)
            zf.write(path, rel_path.as_posix())
    return zip_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Zip a skill directory")
    parser.add_argument("--skills-dir", required=True, help="Path to skill directory")
    parser.add_argument("--zip-name", required=True, help="Zip file name")
    args = parser.parse_args()

    skills_dir = Path(args.skills_dir)
    if not skills_dir.exists():
        raise SystemExit(f"Skill directory not found: {skills_dir}")

    zip_skill_dir(skills_dir, args.zip_name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
