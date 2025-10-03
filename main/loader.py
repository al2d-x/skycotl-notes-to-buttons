#-# loader.py
from __future__ import annotations
from pathlib import Path
from typing import Dict, List, Union
import re

from bs4 import BeautifulSoup

ActiveMap = Dict[int, Union[List[int], str]]

# --- helpers ---------------------------------------------------------------

_ON_PATTERN = re.compile(r"\bON-\d+\b")

def _is_cell_on(svg) -> bool:
    """Return True if any descendant in this <svg> has a class like 'ON-0'."""
    if svg is None:
        return False
    # Fast path: look for ON-* in any class attribute of descendants
    for node in svg.find_all(True):
        classes = node.get("class", [])
        if any(c.startswith("ON-") or c == "ON" for c in classes):
            return True
    # Fallback: text search (robust across odd HTML)
    return bool(_ON_PATTERN.search(str(svg)))

def _field_number_from_td(td, fallback_index: int) -> int:
    """
    Extract the 1..15 field number. Preferred source is the 'button-N' class on the <svg>.
    If missing, fall back to the 1..15 index passed by caller.
    """
    svg = td.find("svg")
    if svg:
        classes = svg.get("class", [])
        for c in classes:
            if c.startswith("button-"):
                try:
                    # HTML uses 0..14; we want 1..15
                    return int(c.split("-", 1)[1]) + 1
                except ValueError:
                    pass
    return fallback_index  # (y-1)*5 + x from caller

# --- public API ------------------------------------------------------------

def load_active_map(html_path: str) -> ActiveMap:
    """
    Parse the HTML at html_path, anchor at <div id="transcript">,
    and return a map: { table_index: [active_field_numbers] }.
    If a table has no active cells, set its value to 'noValue'.
    Table indices start at 1 in the order they appear under #transcript.
    """
    p = Path(html_path)
    if not p.exists():
        raise FileNotFoundError(f"HTML file not found: {p}")

    soup = BeautifulSoup(p.read_text(encoding="utf-8", errors="ignore"), "html.parser")

    root = soup.find(id="transcript")
    if not root:
        raise RuntimeError('Could not find <div id="transcript"> in the HTML.')

    tables = root.select("table.harp")
    result: ActiveMap = {}

    for t_idx, table in enumerate(tables, start=1):
        classes = set(table.get("class", []))
        # Quick skip: explicitly silent table
        if "silent" in classes:
            result[t_idx] = "noValue"
            continue

        active_fields: List[int] = []
        rows = table.find_all("tr")

        # We’ll also compute a fallback 1..15 index based on row/col, just in case
        # left-to-right, top-to-bottom = 5 cols per row.
        for y, row in enumerate(rows, start=1):
            cells = row.find_all("td")
            for x, td in enumerate(cells, start=1):
                svg = td.find("svg")
                # compute fallback field number
                fallback_field_num = (y - 1) * 5 + x  # 1..15
                field_num = _field_number_from_td(td, fallback_field_num)
                if _is_cell_on(svg):
                    active_fields.append(field_num)

        if active_fields:
            # sort & dedupe, just in case the markup repeats shapes inside the same cell
            result[t_idx] = sorted(set(active_fields))
        else:
            result[t_idx] = "noValue"

    return result
