"""
Compile test gettext catalogs so translated URL patterns work on a clean clone.

Repository ``.gitignore`` excludes ``*.mo``; CI and dev environments need ``msgfmt``.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


def pytest_sessionstart(session) -> None:
    if not shutil.which("msgfmt"):
        return
    tests_dir = Path(__file__).resolve().parent
    for po_path in tests_dir.joinpath("locale").rglob("django.po"):
        mo_path = po_path.with_suffix(".mo")
        subprocess.run(
            ["msgfmt", "-o", str(mo_path), str(po_path)],
            check=True,
        )
