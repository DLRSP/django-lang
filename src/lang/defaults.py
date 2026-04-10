"""
Built-in defaults for i18n / SEO helpers.

Runtime resolution (settings + optional ``APP_CONFIG``) lives in
:mod:`lang.conf`; do **not** require projects to import this module from
``settings.py`` unless they prefer explicit re-exports.

``HREFLANG_DEFAULT_LANGUAGE`` is project-specific; set it via
``settings.HREFLANG_DEFAULT_LANGUAGE`` or ``APP_CONFIG['lang']`` (see
:mod:`lang.conf`).
"""

from __future__ import annotations

from typing import Dict

# Google-style BCP 47 in <link hreflang="…"> (Django code → attribute value).
LANGUAGE_HREFLANG_MAP: Dict[str, str] = {
    "zh-hans": "zh-Hans",
    "zh-hant": "zh-Hant",
}

# JSON-LD ``sameAs`` (or similar) → Wikipedia articles per language.
LANGUAGE_WIKIPEDIA_SAMEAS: Dict[str, str] = {
    "it": "https://en.wikipedia.org/wiki/Italian_language",
    "en": "https://en.wikipedia.org/wiki/English_language",
    "de": "https://en.wikipedia.org/wiki/German_language",
    "fr": "https://en.wikipedia.org/wiki/French_language",
    "es": "https://en.wikipedia.org/wiki/Spanish_language",
    "pt": "https://en.wikipedia.org/wiki/Portuguese_language",
    "nl": "https://en.wikipedia.org/wiki/Dutch_language",
    "pl": "https://en.wikipedia.org/wiki/Polish_language",
    "ru": "https://en.wikipedia.org/wiki/Russian_language",
    "zh-hans": "https://en.wikipedia.org/wiki/Chinese_language",
    "ja": "https://en.wikipedia.org/wiki/Japanese_language",
    "ko": "https://en.wikipedia.org/wiki/Korean_language",
    "ar": "https://en.wikipedia.org/wiki/Arabic",
}

# Open Graph ``og:locale``-style strings (underscore + region).
OG_LOCALE_BY_LANGUAGE: Dict[str, str] = {
    "it": "it_IT",
    "en": "en_US",
    "de": "de_DE",
    "fr": "fr_FR",
    "es": "es_ES",
    "pt": "pt_PT",
    "nl": "nl_NL",
    "pl": "pl_PL",
    "ru": "ru_RU",
    "zh-hans": "zh_CN",
    "ja": "ja_JP",
    "ko": "ko_KR",
    "ar": "ar_SA",
}
