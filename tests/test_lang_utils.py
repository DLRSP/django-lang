"""
Scope: lang.utils (hreflang BCP 47 mapping, flag map merge).

Out of scope: template rendering (see other test modules).
"""

from django.template import Context, Template
from django.test import TestCase, override_settings

from lang.utils import build_language_flag_map, get_hreflang_code


class GetHreflangCodeTests(TestCase):
    def test_returns_django_code_when_no_mapping(self):
        with override_settings(LANGUAGE_HREFLANG_MAP=None):
            self.assertEqual(get_hreflang_code("fr"), "fr")

    def test_applies_mapping_when_configured(self):
        with override_settings(
            LANGUAGE_HREFLANG_MAP={"fr": "fr-FR", "zh-hans": "zh-Hans"}
        ):
            self.assertEqual(get_hreflang_code("zh-hans"), "zh-Hans")
            self.assertEqual(get_hreflang_code("de"), "de")


class HreflangBcp47TemplateFilterTests(TestCase):
    def test_hreflang_bcp47_filter_in_template(self):
        with override_settings(LANGUAGE_HREFLANG_MAP={"pt": "pt-BR"}):
            tpl = Template(
                "{% load languages_helpers %}{{ code|hreflang_bcp47 }}"
            )
            out = tpl.render(Context({"code": "pt"}))
            self.assertEqual(out, "pt-BR")


class BuildLanguageFlagMapTests(TestCase):
    def test_user_map_overrides_defaults(self):
        with override_settings(LANGUAGE_FLAG_MAP={"en": "us"}):
            m = build_language_flag_map()
            self.assertEqual(m["en"], "us")
            self.assertEqual(m["zh-hans"], "cn")

    def test_preserves_default_keys_when_user_partial(self):
        with override_settings(LANGUAGE_FLAG_MAP={}):
            m = build_language_flag_map()
            self.assertEqual(m["en"], "gb")
            self.assertIn("ar", m)
