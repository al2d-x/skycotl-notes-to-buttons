#main/mapper.py
"""
Mapping / normalization
=======================
Normalizes loaded active maps:
- keeps only integers 1..15
- sorts and de-duplicates
- converts empty bars to "noValue"
"""


from __future__ import annotations
from typing import Dict, List, Union

ActiveMapIn  = Dict[int, Union[List[int], str]]
ActiveMapOut = Dict[int, Union[List[int], str]]

def map_active_map(active_map: ActiveMapIn, profile: str = "") -> ActiveMapOut:
    """
    Mapping is number-preserving. We simply sanitize to 1..15 and sort/dedupe.
    ('profile' kept for signature compatibility.)
    """
    mapped: ActiveMapOut = {}
    for idx, value in active_map.items():
        if value == "noValue":
            mapped[idx] = "noValue"
            continue
        clean = sorted({n for n in value if isinstance(n, int) and 1 <= n <= 15})
        mapped[idx] = clean if clean else "noValue"
    return mapped
