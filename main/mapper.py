# mapper.py
from __future__ import annotations
from typing import Dict, List, Union, Final

# Immutable, index-aligned lookup (0 is a dummy so 1..15 map directly).
FIELD_LABELS: Final[tuple[str, ...]] = (
    "",                # 0 (unused)
    "LT",              # 1
    "RT",              # 2
    "Dpad_Down",       # 3
    "A",               # 4
    "Dpad_Left",       # 5
    "X",               # 6
    "Dpad_Up",         # 7
    "Y",               # 8
    "Dpad_Right",      # 9
    "B",               # 10
    "LB",       # 11  <-- note the 'button_' prefix in your file list
    "RB",              # 12
    "LeftStick_left",  # 13
    "RightStick_left", # 14
    "LeftStick_Right", # 15
)

ActiveMapIn  = Dict[int, Union[List[int], str]]
ActiveMapOut = Dict[int, Union[List[str], str]]

def map_active_map(active_map: ActiveMapIn) -> ActiveMapOut:
    """
    Convert {table_idx: [field_numbers]} to {table_idx: [labels]}.
    If a table has no active values (or is 'noValue'), keep 'noValue'.
    """
    mapped: ActiveMapOut = {}

    for table_idx, value in active_map.items():
        if value == "noValue":
            mapped[table_idx] = "noValue"
            continue

        # Map numbers -> labels, ignore out-of-range just in case.
        labels = [FIELD_LABELS[n] for n in value if 0 < n < len(FIELD_LABELS)]

        mapped[table_idx] = labels if labels else "noValue"

    return mapped
