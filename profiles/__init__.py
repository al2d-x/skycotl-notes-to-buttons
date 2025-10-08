#profiles/__init__.py

"""
Profiles package
================
Public re-exports for profile discovery/validation and registry access.

Re-exports:
- Profile, ProfileReport
- ASSETS_DIR, PROFILES, get_profile, get_profile_report, refresh_profiles
"""

from .model import Profile, ProfileReport
from .registry import ASSETS_DIR, PROFILES, get_profile, get_profile_report, refresh_profiles
