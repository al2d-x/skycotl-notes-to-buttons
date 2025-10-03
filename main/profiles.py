# profiles.py
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

# Root folder for all UI assets: <repo>/ui
ASSETS_DIR = (Path(__file__).resolve().parents[1] / "ui").resolve()

@dataclass(frozen=True)
class Profile:
    key: str
    label: str
    field_labels: Tuple[str, ...]
    # Map label -> filename INSIDE the profile subfolder (no path).
    # If a label is missing here, we will try "<Label>.png".
    icon_files: Dict[str, str]
    # Subfolder name inside ui/, e.g. "xbox", "ps", "switch", "keyboard"
    asset_subdir: str
    rest_label: str = "Rest"
    text_fallback: bool = False

# ---- label tables ---------------------------------------------------------
FIELD_LABELS_XBOX = (
    "", "LT", "RT", "Dpad_Down", "A", "Dpad_Left", "X", "Dpad_Up",
    "Y", "Dpad_Right", "B", "LB", "RB", "LeftStick_left", "RightStick_left",
    "LeftStick_Right",
)
FIELD_LABELS_PS = (
    "", "L2", "R2", "Dpad_Down", "Cross", "Dpad_Left", "Square", "Dpad_Up",
    "Triangle", "Dpad_Right", "Circle", "L1", "R1", "LeftStick_left",
    "RightStick_left", "LeftStick_Right",
)
FIELD_LABELS_SWITCH = (
    "", "ZL", "ZR", "Dpad_Down", "B", "Dpad_Left", "Y", "Dpad_Up",
    "X", "Dpad_Right", "A", "L", "R", "LeftStick_left", "RightStick_left",
    "LeftStick_Right",
)
FIELD_LABELS_KB_EN = (
    "", "Z", "U", "I", "O", "P", "H", "J", "K", "L", "Ö", "N", "M", ",", ".", "-"
)
FIELD_LABELS_KB_DE = (
    "", "Y", "U", "I", "O", "P", "H", "J", "K", "L", ";", "N", "M", ",", ".", "-"
)

# ---- icon maps ------------------------------------------------------------
ICONS_XBOX = {
    "A": "A.png", "B": "B.png", "X": "X.png", "Y": "Y.png",
    "LB": "LB.png", "RB": "RB.png", "LT": "LT.png", "RT": "RT.png",
    "Dpad_Up": "Dpad_Up.png", "Dpad_Down": "Dpad_Down.png",
    "Dpad_Left": "Dpad_Left.png", "Dpad_Right": "Dpad_Right.png",
    "LeftStick_left": "LeftStick_left.png", "LeftStick_Right": "LeftStick_Right.png",
    "RightStick_left": "RightStick_left.png",
}
ICONS_PS: Dict[str, str] = {}       # use "<Label>.png" fallback in /ui/ps
ICONS_SWITCH: Dict[str, str] = {}   # use "<Label>.png" fallback in /ui/switch
ICONS_KEYBOARD: Dict[str, str] = {} # keyboard uses text badges by default

PROFILES: Dict[str, Profile] = {
    "xbox": Profile(
        key="xbox",
        label="Xbox / PC",
        field_labels=FIELD_LABELS_XBOX,
        icon_files=ICONS_XBOX,
        asset_subdir="xbox",    
        rest_label="Rest",
        text_fallback=False,
    ),
    "ps": Profile(
        key="ps",
        label="PlayStation",
        field_labels=FIELD_LABELS_PS,
        icon_files=ICONS_PS,
        asset_subdir="ps",       
        rest_label="Rest",
        text_fallback=False,
    ),
    "switch": Profile(
        key="switch",
        label="Switch",
        field_labels=FIELD_LABELS_SWITCH,
        icon_files=ICONS_SWITCH,
        asset_subdir="switch",   
        rest_label="Rest",
        text_fallback=False,
    ),
    "kb_en": Profile(
        key="kb_en",
        label="Keyboard (EN)",
        field_labels=FIELD_LABELS_KB_EN,
        icon_files=ICONS_KEYBOARD,
        asset_subdir="keyboard",     
        rest_label="Rest",
        text_fallback=True,
    ),
    "kb_de": Profile(
        key="kb_de",
        label="Keyboard (DE)",
        field_labels=FIELD_LABELS_KB_DE,
        icon_files=ICONS_KEYBOARD,
        asset_subdir="keyboard",    
        rest_label="Rest",
        text_fallback=True,
    ),
}


def get_profile(key: str) -> Profile:
    return PROFILES.get(key, PROFILES["xbox"])
