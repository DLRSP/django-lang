"""
Context processors for django-lang app
"""

from typing import Any, Dict

from django.conf import settings

from lang.conf import (
    get_hreflang_default_language,
    get_language_wikipedia_sameas,
    get_og_locale_by_language,
)


def from_settings(request) -> Dict[str, Any]:
    return {
        "DEFAULT_LANGUAGE_CODE": getattr(settings, attr, None)
        for attr in ("LANGUAGE_CODE",)
    }


def language_switcher_next(request) -> Dict[str, Any]:
    """
    Optional: set ``redirect_to`` to the current path for packaged language forms
    (``set_language`` POST field ``next``). Add to ``TEMPLATES`` context_processors
    when you use ``lang/nav-link.html`` without
    passing ``redirect_to`` from each view.
    """
    if request is None:
        return {}
    return {"redirect_to": request.get_full_path()}


def seo_i18n(request) -> Dict[str, Any]:
    """
    SEO helpers for multilingual templates (list **after**
    ``lang.context_processors.from_settings`` so it can override
    ``DEFAULT_LANGUAGE_CODE`` when needed).

    - ``DEFAULT_LANGUAGE_CODE``: set from ``settings.HREFLANG_DEFAULT_LANGUAGE``
      when it is a non-empty string (drives ``hreflang.html`` ``x-default``).
      If unset or empty, ``from_settings`` keeps ``LANGUAGE_CODE``.
    - ``LANGUAGE_WIKIPEDIA_SAMEAS``: optional ``dict`` mapping Django language
      code → URL (e.g. JSON-LD ``sameAs`` for languages).
    - ``OG_LOCALE_BY_LANGUAGE``: optional ``dict`` mapping Django language code
      → Open Graph locale string (e.g. ``it_IT``).

    Configure on ``settings`` (all optional except the first, which is
    opt-in via defining ``HREFLANG_DEFAULT_LANGUAGE``):

    - ``HREFLANG_DEFAULT_LANGUAGE`` (top-level or ``APP_CONFIG['lang']``)
    - ``LANGUAGE_WIKIPEDIA_SAMEAS`` / ``OG_LOCALE_BY_LANGUAGE`` (same)

    See :mod:`lang.conf` for merge rules.
    """
    ctx: Dict[str, Any] = {
        "LANGUAGE_WIKIPEDIA_SAMEAS": get_language_wikipedia_sameas(),
        "OG_LOCALE_BY_LANGUAGE": get_og_locale_by_language(),
    }
    href_default = get_hreflang_default_language()
    if href_default:
        ctx["DEFAULT_LANGUAGE_CODE"] = href_default
    return ctx
