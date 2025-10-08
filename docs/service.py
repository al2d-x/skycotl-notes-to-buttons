#docs/services

"""
Docs service
============
Provides filesystem helpers to read local documentation and enumerate license
files without any network access. Used by the GUI to render About/Help content.

Key class:
- DocsService: resolves candidate docs roots and reads text files safely.
"""

from __future__ import annotations
from pathlib import Path
import sys

DOCS_SUBDIR = "docs"
LICENSES_SUBDIR = "licenses"

class DocsService:
    def __init__(self, docs_subdir: str = DOCS_SUBDIR, licenses_subdir: str = LICENSES_SUBDIR):
        self.docs_subdir = docs_subdir
        self.licenses_subdir = licenses_subdir

    def _candidate_roots(self) -> list[Path]:
        here = Path(__file__).resolve()
        c: list[Path] = []
        if getattr(sys, "frozen", False):
            exe_dir = Path(sys.executable).resolve().parent
            c += [exe_dir / self.docs_subdir]
        c += [here.parents[2] / self.docs_subdir, here.parents[1] / self.docs_subdir, Path.cwd() / self.docs_subdir]
        seen, out = set(), []
        for p in c:
            if p not in seen:
                seen.add(p)
                out.append(p)
        return out

    def read_text(self, relpath: str) -> str:
        for root in self._candidate_roots():
            p = (root / relpath)
            try:
                if p.is_file():
                    return p.read_text(encoding="utf-8")
            except Exception:
                pass
        return ""

    def list_license_files(self) -> list[Path]:
        files: list[Path] = []
        for root in self._candidate_roots():
            lic_dir = root / self.licenses_subdir
            if lic_dir.is_dir():
                files.extend(sorted(lic_dir.glob("*.txt")))
        return files
