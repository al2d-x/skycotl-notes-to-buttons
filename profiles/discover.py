#profiles/discover.py
"""
Profiles: discovery
===================
Finds the icon assets root and enumerates profile directories. Reads optional
`profile.json` per profile to fill label and display names.

Exports:
- resolve_assets_root() -> Path
- discover_profiles(root: Path) -> Dict[str, Profile]
"""

from __future__ import annotations
from pathlib import Path
from typing import Dict, Tuple
import json, sys

from .model import Profile

def _candidate_roots() -> list[Path]:
    here = Path(__file__).resolve()
    c: list[Path] = []
    if getattr(sys, "frozen", False):
        exe_dir = Path(sys.executable).resolve().parent
        c += [exe_dir / "sntb-ui", exe_dir / "sntb_ui", exe_dir / "ui", exe_dir / "assets" / "sntb-ui"]
    c += [here.parents[2] / "sntb-ui", here.parents[2] / "sntb_ui", here.parents[2] / "ui", here.parents[1] / "sntb-ui"]
    cwd = Path.cwd()
    c += [cwd / "sntb-ui", cwd / "sntb_ui", cwd / "ui", cwd / "assets" / "sntb-ui"]
    seen, out = set(), []
    for p in c:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out

def resolve_assets_root() -> Path:
    for c in _candidate_roots():
        if c.is_dir():
            return c.resolve()
    return Path("sntb-ui").resolve()

def _load_profile_meta(dir_path: Path) -> Tuple[str, dict[int, str], str]:
    label = dir_path.name
    names: dict[int, str] = {}
    rest_label = "Rest"
    meta = dir_path / "profile.json"
    if meta.exists():
        try:
            data = json.loads(meta.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                label = data.get("label", label)
                rest_label = data.get("rest_label", rest_label)
                if isinstance(data.get("names"), dict):
                    for k, v in data["names"].items():
                        try:
                            n = int(k)
                            if 1 <= n <= 15 and isinstance(v, str):
                                names[n] = v
                        except Exception:
                            pass
        except Exception:
            pass
    return label, names, rest_label

def _dir_looks_like_profile(p: Path) -> bool:
    if not p.is_dir() or p.name.startswith("."):
        return False
    if (p / "profile.json").exists():
        return True
    try:
        return any(child.is_file() and child.suffix.lower() == ".png" for child in p.iterdir())
    except Exception:
        return False

def discover_profiles(root: Path) -> Dict[str, Profile]:
    profiles: Dict[str, Profile] = {}
    if not root.exists():
        return profiles
    for child in sorted(root.iterdir()):
        if _dir_looks_like_profile(child):
            key = child.name
            label, names, rest_label = _load_profile_meta(child)
            profiles[key] = Profile(
                key=key, label=label, asset_dir=child.resolve(), names=names, rest_label=rest_label, text_fallback=True
            )
    return profiles
