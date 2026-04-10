"""
Shared helpers for language display (hreflang BCP 47, flag region codes).

Resolved values come from :mod:`lang.conf` (settings + ``APP_CONFIG`` + defaults).
"""

from __future__ import annotations

from typing import Dict

# Reasonable defaults for common Django language codes (ISO 3166-1 for flag.emoji).
DEFAULT_LANGUAGE_FLAG_MAP: Dict[str, str] = {
    "ar": "sa",
    "en": "gb",
    "ja": "jp",
    "ko": "kr",
    "pt": "pt",
    "ru": "ru",
    "zh-hans": "cn",
    "zh-hant": "tw",
}


def get_hreflang_code(django_language_code: str) -> str:
    """Return the hreflang attribute value for a Django ``LANGUAGE_CODE``."""
    from lang.conf import get_language_hreflang_map

    return get_language_hreflang_map().get(
        django_language_code, django_language_code
    )


def build_language_flag_map() -> Dict[str, str]:
    """Merge built-in flag regions with project / ``APP_CONFIG`` overrides."""
    from lang.conf import get_language_flag_map

    return get_language_flag_map()
