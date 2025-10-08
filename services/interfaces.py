#services/interfaces.py
"""
Service interfaces (Protocols)
==============================
Minimal call-signatures for the conversion pipeline. Kept tiny on purpose
to make testing and swapping implementations trivial.

Protocols:
- Loader(html_path) -> ActiveMap
- Mapper(active_map, profile) -> ActiveMap
- Exporter(mapping, out_html, title, profile) -> Path
"""


from __future__ import annotations
from typing import Protocol, Dict, Union, List
from pathlib import Path

ActiveMap = Dict[int, Union[List[int], str]]

class Loader(Protocol):
    def __call__(self, html_path: str) -> ActiveMap: ...

class Mapper(Protocol):
    def __call__(self, active_map: ActiveMap, profile: str = "") -> ActiveMap: ...

class Exporter(Protocol):
    def __call__(self, mapping: ActiveMap, out_html: str | Path, title: str, profile: str) -> Path: ...
