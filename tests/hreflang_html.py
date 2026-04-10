"""Parse ``<link rel="alternate" hreflang="…" href="…">`` from rendered hreflang.html."""

from __future__ import annotations

import re
from typing import List, Tuple

# Matches the attribute order emitted by ``lang/templates/hreflang.html``.
_ALTERNATE_LINK_RE = re.compile(
    r'<link\s+rel="alternate"\s+hreflang="([^"]+)"\s+href="([^"]+)"\s*/>',
)


def parse_alternate_links(html: str) -> List[Tuple[str, str]]:
    """Return list of (hreflang_attribute, href) for each alternate link."""
    return _ALTERNATE_LINK_RE.findall(html)
