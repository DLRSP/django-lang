"""
Optional middleware for Django's ``set_language`` view and gettext_lazy URL paths.

``django.views.i18n.set_language`` calls ``django.urls.translate_url``, which runs
``resolve()`` while the **active** translation language is still the one chosen by
``LocaleMiddleware`` for the current request. For POSTs to ``/i18n/setlang/`` there
is no language prefix in the URL, so the language often comes from the
``django_language`` cookie (e.g. ``LANGUAGE_CODE`` default ``en``). If the user is
leaving a page whose path uses a **different** prefix (e.g. ``/it/...``) and
translated segments from ``gettext_lazy``, ``resolve()`` can fail under the wrong
active language and the redirect keeps the old prefix — while the cookie updates,
``LocaleMiddleware`` still prefers the URL prefix, so the UI appears stuck.

This middleware activates the language parsed from the ``next`` URL path (when it
carries an i18n prefix) **before** ``set_language`` runs, so ``translate_url`` matches
the same patterns as for a normal request on that path.

Insert **immediately after** ``django.middleware.locale.LocaleMiddleware``::

    MIDDLEWARE = [
        ...
        "django.middleware.locale.LocaleMiddleware",
        "lang.middleware.SetLanguageNextPathMiddleware",
        ...
    ]
"""

from __future__ import annotations

from urllib.parse import urlsplit

from django.utils import translation
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import get_language_from_path


class SetLanguageNextPathMiddleware(MiddlewareMixin):
    """Align active language with the i18n prefix in ``next`` for POST ``set_language``."""

    def process_request(self, request):
        if request.method != "POST":
            return None
        path_info = request.path_info or ""
        if not path_info.startswith("/i18n/") or "setlang" not in path_info:
            return None
        next_url = request.POST.get("next") or request.GET.get("next")
        if not next_url:
            return None
        path = urlsplit(next_url).path or "/"
        path_lang = get_language_from_path(path)
        if not path_lang:
            return None
        translation.activate(path_lang)
        if hasattr(request, "LANGUAGE_CODE"):
            request.LANGUAGE_CODE = path_lang
        return None
