#profiles/model.py
"""
Profiles: model types
=====================
Dataclasses for profile metadata and validation results.

Classes:
- Profile: folder key, label, icon paths, display names, etc.
- ProfileReport: validation outcome (missing/extras/problems).
"""

from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Optional, List, Set

@dataclass(frozen=True)
class Profile:
    key: str
    label: str
    asset_dir: Path
    names: Mapping[int, str]
    rest_label: str = "Rest"
    text_fallback: bool = True

    def icon_path(self, number: int) -> Optional[Path]:
        if not (1 <= number <= 15):
            return None
        p = (self.asset_dir / f"{number}.png").resolve()
        return p if p.exists() else None

    def display_name_for(self, number: int) -> str:
        return self.names.get(number, str(number))

@dataclass(frozen=True)
class ProfileReport:
    key: str
    valid: bool
    missing: Set[int]
    extras: List[str]
    problems: List[str]
