"""lang.conf: settings + APP_CONFIG + defaults resolution."""

from django.test import TestCase, override_settings

from lang import defaults
from lang.conf import (
    get_hreflang_default_language,
    get_language_flag_map,
    get_language_hreflang_map,
)


class ConfTestCase(TestCase):
    def test_get_language_hreflang_map_uses_defaults(self):
        m = get_language_hreflang_map()
        self.assertEqual(m["zh-hans"], "zh-Hans")

    def test_get_hreflang_default_from_top_level_setting(self):
        with override_settings(HREFLANG_DEFAULT_LANGUAGE="de"):
            self.assertEqual(get_hreflang_default_language(), "de")

    def test_get_hreflang_default_from_app_config_when_top_empty(self):
        with override_settings(
            HREFLANG_DEFAULT_LANGUAGE="",
            APP_CONFIG={"lang": {"HREFLANG_DEFAULT_LANGUAGE": "pt"}},
        ):
            self.assertEqual(get_hreflang_default_language(), "pt")

    def test_top_level_hreflang_default_wins_over_app_config(self):
        with override_settings(
            HREFLANG_DEFAULT_LANGUAGE="fr",
            APP_CONFIG={"lang": {"HREFLANG_DEFAULT_LANGUAGE": "it"}},
        ):
            self.assertEqual(get_hreflang_default_language(), "fr")

    @override_settings(
        APP_CONFIG={
            "lang": {
                "LANGUAGE_HREFLANG_MAP": {"en": "en-GB"},
            }
        }
    )
    def test_app_config_partial_merges_onto_defaults(self):
        m = get_language_hreflang_map()
        self.assertEqual(m["en"], "en-GB")
        self.assertEqual(m["zh-hans"], defaults.LANGUAGE_HREFLANG_MAP["zh-hans"])

    @override_settings(LANGUAGE_HREFLANG_MAP={"de": "de-DE"})
    def test_top_level_setting_replaces_hreflang_map_entirely(self):
        m = get_language_hreflang_map()
        self.assertEqual(m, {"de": "de-DE"})
        self.assertNotIn("zh-hans", m)

    @override_settings(
        LANGUAGE_FLAG_MAP={"en": "us"},
        APP_CONFIG={"lang": {"LANGUAGE_FLAG_MAP": {"it": "it"}}},
    )
    def test_flag_map_merges_settings_then_app_config(self):
        m = get_language_flag_map()
        self.assertEqual(m["en"], "us")
        self.assertEqual(m["it"], "it")
        self.assertEqual(m["ja"], "jp")
