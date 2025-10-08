#profiles/validate.py
"""
Profiles: validation
====================
Validates a profile directory:
- checks presence of 1.png..15.png
- flags out-of-range numbered files
- builds a human-readable problem list.

Exports:
- report_for(profile: Profile) -> ProfileReport
"""

from __future__ import annotations
from pathlib import Path
import re
from typing import List, Set

from .model import Profile, ProfileReport

_NUM_RE = re.compile(r"^(\d+)\.png$", re.IGNORECASE)

def report_for(profile: Profile) -> ProfileReport:
    present = {n for n in range(1, 16) if (profile.asset_dir / f"{n}.png").exists()}
    missing = {n for n in range(1, 16) if n not in present}

    extras: List[str] = []
    try:
        for child in profile.asset_dir.glob("*.png"):
            m = _NUM_RE.match(child.name)
            if m:
                try:
                    num = int(m.group(1))
                    if num < 1 or num > 15:
                        extras.append(child.name)
                except Exception:
                    pass
    except Exception:
        pass

    problems: List[str] = []
    if not present:
        problems.append("No numbered icons found (expected 1.png–15.png).")
    if missing:
        problems.append(
            f"Missing icons: {', '.join(map(str, sorted(missing)))}." if len(missing) <= 6 else f"{len(missing)} numbered icons missing."
        )
    if extras:
        problems.append(
            "Out-of-range files: " + ", ".join(sorted(extras)) + "." if len(extras) <= 6 else f"{len(extras)} out-of-range numbered files present."
        )

    valid = (not missing) and (not extras)
    return ProfileReport(
        key=profile.key, valid=valid, missing=missing, extras=extras, problems=problems or (["OK"] if valid else []),
    )
