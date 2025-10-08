#services/conversion.py
"""
Conversion service
==================
Thin orchestrator that wires loader → mapper → exporter into one call.

Class:
- ConversionService: convert(in_file, out_file, title, profile) -> Path
"""

from __future__ import annotations
from pathlib import Path
from .interfaces import Loader, Mapper, Exporter, ActiveMap

class ConversionService:
    def __init__(self, loader: Loader, mapper: Mapper, exporter: Exporter):
        self.loader = loader
        self.mapper = mapper
        self.exporter = exporter

    def convert(self, in_file: str, out_file: str | Path, title: str, profile: str) -> Path:
        raw: ActiveMap = self.loader(in_file)
        mapped: ActiveMap = self.mapper(raw, profile=profile)
        out_path: Path = self.exporter(mapped, out_file, title=title, profile=profile)
        return out_path
