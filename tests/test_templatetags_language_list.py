"""
Scope: get_language_info_list_ex (nav-link language rows: codes, flags, bidi, labels).

Out of scope: translate_url, hreflang.html markup, URL routing.

LANGUAGE_FLAG_MAP / defaults: see test_lang_utils.py and ``test_flag_map_respects_settings_override``.
"""

from django.conf import settings
from django.test import TestCase, override_settings
from django.utils import translation

from lang.templatetags.languages_helpers import get_language_info_list_ex


class GetLanguageInfoListExTests(TestCase):
    """Filter used by lang/nav-link.html: one row per settings.LANGUAGES entry."""

    def test_returns_all_language_codes(self):
        translation.activate("it")
        self.addCleanup(translation.deactivate)
        request = self.client.get("/it/").wsgi_request
        rows = get_language_info_list_ex(request)
        codes = {r["code"] for r in rows}
        expected = {code for code, _ in settings.LANGUAGES}
        self.assertEqual(codes, expected)

    def test_current_language_marked(self):
        translation.activate("de")
        self.addCleanup(translation.deactivate)
        request = self.client.get("/de/").wsgi_request
        rows = get_language_info_list_ex(request)
        by_code = {r["code"]: r for r in rows}
        self.assertTrue(by_code["de"]["is_current"])
        self.assertFalse(by_code["it"]["is_current"])

    def test_arabic_is_bidi(self):
        translation.activate("en")
        self.addCleanup(translation.deactivate)
        request = self.client.get("/en/").wsgi_request
        rows = get_language_info_list_ex(request)
        ar = next(r for r in rows if r["code"] == "ar")
        self.assertTrue(ar["bidi"])

    def test_each_row_has_flag_and_names(self):
        translation.activate("en")
        self.addCleanup(translation.deactivate)
        request = self.client.get("/en/").wsgi_request
        rows = get_language_info_list_ex(request)
        for r in rows:
            self.assertIn("code", r)
            self.assertIn("flag", r)
            self.assertTrue(len(r["flag"]) >= 1)
            self.assertIn("name", r)
            self.assertIn("name_local", r)
            self.assertIn("name_translated", r)

    def test_zh_hans_present_with_hyphenated_code(self):
        translation.activate("en")
        self.addCleanup(translation.deactivate)
        request = self.client.get("/en/").wsgi_request
        rows = get_language_info_list_ex(request)
        codes = [r["code"] for r in rows]
        self.assertIn("zh-hans", codes)

    def test_flag_map_respects_settings_override(self):
        """LANGUAGE_FLAG_MAP overrides DEFAULT_LANGUAGE_FLAG_MAP (e.g. en → US flag)."""
        translation.activate("de")
        self.addCleanup(translation.deactivate)
        with override_settings(LANGUAGE_FLAG_MAP={}):
            req_default = self.client.get("/de/").wsgi_request
            default_flag = next(
                r["flag"]
                for r in get_language_info_list_ex(req_default)
                if r["code"] == "en"
            )
        with override_settings(LANGUAGE_FLAG_MAP={"en": "us"}):
            req_us = self.client.get("/de/").wsgi_request
            us_flag = next(
                r["flag"]
                for r in get_language_info_list_ex(req_us)
                if r["code"] == "en"
            )
        self.assertNotEqual(default_flag, us_flag)
