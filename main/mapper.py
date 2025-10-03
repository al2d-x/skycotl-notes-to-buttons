#-# mapper.py
from __future__ import annotations
from typing import Dict, List, Union
from profiles import get_profile

ActiveMapIn  = Dict[int, Union[List[int], str]]
ActiveMapOut = Dict[int, Union[List[str], str]]

def map_active_map(active_map: ActiveMapIn, profile: str = "xbox") -> ActiveMapOut:
    """
    Convert {table_idx: [field_numbers]} -> {table_idx: [labels]} using the
    chosen profile. 'noValue' is preserved.
    """
    prof = get_profile(profile)
    table = prof.field_labels

    mapped: ActiveMapOut = {}
    for table_idx, value in active_map.items():
        if value == "noValue":
            mapped[table_idx] = "noValue"
            continue
        labels = [table[n] for n in value if 0 < n < len(table)]
        mapped[table_idx] = labels if labels else "noValue"
    return mapped
