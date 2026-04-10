"""
Resolved configuration for ``lang`` (lazy reads from ``django.conf.settings``).

Priority for each value:

1. Top-level Django setting (e.g. ``LANGUAGE_HREFLANG_MAP``), if set.
2. Partial override inside ``settings.APP_CONFIG["lang"]`` merged onto
   :mod:`lang.defaults`.
3. Package defaults from :mod:`lang.defaults`.

Projects can rely on defaults only (no imports from ``lang.defaults`` in
``settings.py``) and optionally set::

    APP_CONFIG = {
        "lang": {
            "HREFLANG_DEFAULT_LANGUAGE": "it",
            "LANGUAGE_HREFLANG_MAP": {"en": "en-GB"},
        },
    }
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from django.conf import settings

from lang import defaults


def _app_config_lang() -> Dict[str, Any]:
    cfg = getattr(settings, "APP_CONFIG", None) or {}
    lang = cfg.get("lang")
    return dict(lang) if lang else {}


def _merged_lang_dict(
    setting_name: str,
    defaults_dict: Dict[str, str],
) -> Dict[str, str]:
    """
    Full replacement if ``settings.<name>`` is set; else defaults merged with
    ``APP_CONFIG['lang'][<name>]`` (partial).
    """
    explicit = getattr(settings, setting_name, None)
    if explicit is not None:
        return dict(explicit)
    partial = _app_config_lang().get(setting_name)
    if partial:
        return {**defaults_dict, **dict(partial)}
    return dict(defaults_dict)


def get_language_hreflang_map() -> Dict[str, str]:
    """Django language code → BCP 47 ``hreflang`` attribute value."""
    return _merged_lang_dict(
        "LANGUAGE_HREFLANG_MAP",
        defaults.LANGUAGE_HREFLANG_MAP,
    )


def get_language_wikipedia_sameas() -> Dict[str, str]:
    """Django language code → Wikipedia URL (e.g. JSON-LD ``sameAs``)."""
    return _merged_lang_dict(
        "LANGUAGE_WIKIPEDIA_SAMEAS",
        defaults.LANGUAGE_WIKIPEDIA_SAMEAS,
    )


def get_og_locale_by_language() -> Dict[str, str]:
    """Django language code → Open Graph locale string."""
    return _merged_lang_dict(
        "OG_LOCALE_BY_LANGUAGE",
        defaults.OG_LOCALE_BY_LANGUAGE,
    )


def get_hreflang_default_language() -> Optional[str]:
    """
    Brand default for ``hreflang`` ``x-default`` (non-empty string or ``None``).

    Reads ``HREFLANG_DEFAULT_LANGUAGE`` from top-level settings, then
    ``APP_CONFIG['lang']['HREFLANG_DEFAULT_LANGUAGE']``.
    """
    top = getattr(settings, "HREFLANG_DEFAULT_LANGUAGE", None)
    if top:
        return str(top)
    nested = _app_config_lang().get("HREFLANG_DEFAULT_LANGUAGE")
    if nested:
        return str(nested)
    return None


def get_language_flag_map() -> Dict[str, str]:
    """
    ISO region codes for emoji flags: merge package defaults with
    ``settings.LANGUAGE_FLAG_MAP`` and ``APP_CONFIG['lang']['LANGUAGE_FLAG_MAP']``.
    """
    from lang.utils import DEFAULT_LANGUAGE_FLAG_MAP

    user = getattr(settings, "LANGUAGE_FLAG_MAP", None) or {}
    user2 = _app_config_lang().get("LANGUAGE_FLAG_MAP") or {}
    return {**DEFAULT_LANGUAGE_FLAG_MAP, **dict(user), **dict(user2)}
