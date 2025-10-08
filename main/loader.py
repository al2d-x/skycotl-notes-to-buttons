#main/loader.py
"""
HTML loader
===========
Parses saved Sky HTML and extracts "active note" maps per bar.

Exports:
- load_active_map(html_path) -> Dict[int, Union[List[int], "noValue"]]
  Returns a map from bar index to active field numbers (1..15), or "noValue"
  when the bar is silent.
"""


from __future__ import annotations
from pathlib import Path
from typing import Dict, List, Union
import re

from bs4 import BeautifulSoup

ActiveMap = Dict[int, Union[List[int], str]]

_ON_PATTERN = re.compile(r"\bON-\d+\b")

def _is_cell_on(svg) -> bool:
    """Return True if any descendant in this <svg> has a class like 'ON-0'."""
    if svg is None:
        return False
    for node in svg.find_all(True):
        classes = node.get("class", [])
        if any(c.startswith("ON-") or c == "ON" for c in classes):
            return True
    return bool(_ON_PATTERN.search(str(svg)))

def _field_number_from_td(td, fallback_index: int) -> int:
    """
    Extract the 1..15 field number. Prefer 'button-N' on the <svg>;
    otherwise fall back to the supplied index.
    """
    svg = td.find("svg")
    if svg:
        classes = svg.get("class", [])
        for c in classes:
            if c.startswith("button-"):
                try:
                    return int(c.split("-", 1)[1]) + 1  # HTML uses 0..14
                except ValueError:
                    pass
    return fallback_index  # (y-1)*5 + x from caller

def load_active_map(html_path: str) -> ActiveMap:
    """
    Parse the HTML and return { table_index: [active_field_numbers] }.
    If a table has no active cells, set value to 'noValue'.
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
        if "silent" in classes:
            result[t_idx] = "noValue"
            continue

        active_fields: List[int] = []
        rows = table.find_all("tr")

        for y, row in enumerate(rows, start=1):
            cells = row.find_all("td")
            for x, td in enumerate(cells, start=1):
                svg = td.find("svg")
                fallback_field_num = (y - 1) * 5 + x  # 1..15
                field_num = _field_number_from_td(td, fallback_field_num)
                if _is_cell_on(svg):
                    active_fields.append(field_num)

        result[t_idx] = sorted(set(active_fields)) if active_fields else "noValue"

    return result
