"""
Regression: ``set_language`` + ``django.urls.translate_url`` with gettext_lazy paths.

When ``LANGUAGE_CODE`` defaults to ``en`` and ``django_language`` is ``en``, a POST to
``/i18n/setlang/`` has no URL prefix; ``LocaleMiddleware`` activates ``en``. Then
``translate_url("/it/oggetto/…", "de")`` calls ``resolve()`` while lazy URL patterns
are compiled for ``en``, so ``/it/oggetto/…`` does not resolve and the redirect
stays on the Italian path. The language cookie may still update, but the active
language for the *next* GET is driven by the ``/it/`` prefix, so the switch looks
broken.

``lang.middleware.SetLanguageNextPathMiddleware`` activates the language taken from
the ``next`` path prefix before ``set_language`` runs.

Unrelated site issues (e.g. missing migrations / 500) can look similar; these tests
only cover the i18n resolution contract.
"""

from django.test import Client, TestCase, override_settings
from django.urls import translate_url as django_translate_url
from django.utils import translation

import tests.settings as test_settings


def _middleware_without_next_path() -> tuple[str, ...]:
    return tuple(
        m
        for m in test_settings.MIDDLEWARE
        if m != "lang.middleware.SetLanguageNextPathMiddleware"
    )


class DjangoTranslateUrlActiveLanguageMismatchTests(TestCase):
    """Documents ``django.urls.translate_url`` dependency on ``translation.get_language()``."""

    def test_translate_url_noop_when_active_language_mismatches_url_prefix(
        self,
    ):
        """With ``en`` active, Italian translated segment path does not resolve."""
        url = "/it/oggetto/shared-mismatch/"
        translation.activate("en")
        self.addCleanup(translation.deactivate)
        out = django_translate_url(url, "de")
        self.assertEqual(
            out,
            url,
            msg=(
                "Expected unchanged URL when resolve() fails under wrong active language; "
                "see django.urls.translate_url / gettext_lazy patterns."
            ),
        )

    def test_translate_url_translates_when_active_language_matches_prefix(self):
        translation.activate("it")
        self.addCleanup(translation.deactivate)
        out = django_translate_url("/it/oggetto/shared-mismatch/", "de")
        self.assertEqual(out, "/de/artikel/shared-mismatch/")

    def test_translate_url_preserves_query_string_when_fixed(self):
        translation.activate("it")
        self.addCleanup(translation.deactivate)
        out = django_translate_url("/it/oggetto/q/?utm=1", "de")
        self.assertEqual(out, "/de/artikel/q/?utm=1")


class SetLanguagePostRedirectTranslatedPathTests(TestCase):
    """Integration: POST ``set_language`` with ``django_language=en`` cookie."""

    def setUp(self):
        super().setUp()
        self.client = Client(enforce_csrf_checks=False)

    def test_post_redirects_to_target_language_path_with_middleware(self):
        self.client.cookies["django_language"] = "en"
        response = self.client.post(
            "/i18n/setlang/",
            {"next": "/it/oggetto/post-mw/", "language": "de"},
            HTTP_HOST="testserver",
        )
        self.assertEqual(response.status_code, 302)
        loc = response["Location"]
        self.assertIn("/de/artikel/post-mw/", loc)

    @override_settings(MIDDLEWARE=_middleware_without_next_path())
    def test_post_keeps_italian_path_when_middleware_disabled(self):
        """Without ``SetLanguageNextPathMiddleware``, redirect does not translate prefix."""
        self.client.cookies["django_language"] = "en"
        response = self.client.post(
            "/i18n/setlang/",
            {"next": "/it/oggetto/post-nomw/", "language": "de"},
            HTTP_HOST="testserver",
        )
        self.assertEqual(response.status_code, 302)
        loc = response["Location"]
        self.assertIn("/it/oggetto/post-nomw/", loc)
        self.assertNotIn("/de/", loc)
