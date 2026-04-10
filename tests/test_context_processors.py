"""
Scope: lang.context_processors (values injected for templates).

Out of scope: template rendering, translate_url, hreflang markup.
"""

from django.test import TestCase, override_settings

from lang.context_processors import from_settings, language_switcher_next, seo_i18n


class ContextProcessorTests(TestCase):
    def test_from_settings_exposes_default_language_code(self):
        request = self.client.get("/en/").wsgi_request
        ctx = from_settings(request)
        self.assertEqual(ctx["DEFAULT_LANGUAGE_CODE"], "en")

    def test_language_switcher_next_sets_redirect_to_path(self):
        request = self.client.get("/it/demo/nav-link/?q=1").wsgi_request
        ctx = language_switcher_next(request)
        self.assertEqual(ctx["redirect_to"], "/it/demo/nav-link/?q=1")

    @override_settings(
        HREFLANG_DEFAULT_LANGUAGE="it",
        LANGUAGE_WIKIPEDIA_SAMEAS={"it": "https://example.org/wiki/it"},
        OG_LOCALE_BY_LANGUAGE={"it": "it_IT"},
    )
    def test_seo_i18n_sets_default_language_and_dicts(self):
        request = self.client.get("/en/").wsgi_request
        ctx = seo_i18n(request)
        self.assertEqual(ctx["DEFAULT_LANGUAGE_CODE"], "it")
        self.assertEqual(
            ctx["LANGUAGE_WIKIPEDIA_SAMEAS"],
            {"it": "https://example.org/wiki/it"},
        )
        self.assertEqual(ctx["OG_LOCALE_BY_LANGUAGE"], {"it": "it_IT"})

    @override_settings(HREFLANG_DEFAULT_LANGUAGE="")
    def test_seo_i18n_skips_default_language_when_hreflang_setting_empty(self):
        from lang.defaults import LANGUAGE_WIKIPEDIA_SAMEAS, OG_LOCALE_BY_LANGUAGE

        request = self.client.get("/en/").wsgi_request
        ctx = seo_i18n(request)
        self.assertNotIn("DEFAULT_LANGUAGE_CODE", ctx)
        self.assertEqual(ctx["LANGUAGE_WIKIPEDIA_SAMEAS"], LANGUAGE_WIKIPEDIA_SAMEAS)
        self.assertEqual(ctx["OG_LOCALE_BY_LANGUAGE"], OG_LOCALE_BY_LANGUAGE)
