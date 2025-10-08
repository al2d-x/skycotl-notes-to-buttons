#profiles/registry.py
"""
Profiles: in-memory registry
============================
Holds the discovered profiles and precomputed validation reports.
Provides helpers to fetch and refresh the registry.

Exports:
- ASSETS_DIR
- PROFILES: Dict[str, Profile]
- get_profile(key) -> Profile
- get_profile_report(key) -> ProfileReport
- refresh_profiles() -> Dict[str, Profile]
"""

from __future__ import annotations
from typing import Dict

from .discover import resolve_assets_root, discover_profiles
from .validate import report_for
from .model import Profile, ProfileReport

ASSETS_DIR = resolve_assets_root()
PROFILES: Dict[str, Profile] = discover_profiles(ASSETS_DIR)
PROFILE_REPORTS: Dict[str, ProfileReport] = {k: report_for(v) for k, v in PROFILES.items()}

def get_profile(key: str) -> Profile:
    if key in PROFILES:
        return PROFILES[key]
    if PROFILES:
        return PROFILES[sorted(PROFILES.keys())[0]]
    # synthetic empty
    from pathlib import Path
    return Profile(key="(none)", label="(no profiles found)", asset_dir=ASSETS_DIR or Path("."), names={}, rest_label="Rest", text_fallback=True)

def get_profile_report(key: str) -> ProfileReport:
    return PROFILE_REPORTS.get(key) or report_for(get_profile(key))

def refresh_profiles() -> Dict[str, Profile]:
    """Re-discover profiles and rebuild reports; returns the new registry."""
    global PROFILES, PROFILE_REPORTS
    PROFILES = discover_profiles(ASSETS_DIR)
    PROFILE_REPORTS = {k: report_for(v) for k, v in PROFILES.items()}
    return PROFILES
