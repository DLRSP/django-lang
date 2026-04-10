"""
Scope: URL routing under i18n_patterns (language prefix), object detail, set_language route.

Out of scope here: template tags, hreflang/nav templates, context processors.
"""

from django.test import TestCase
from django.urls import reverse


class I18nRoutingTests(TestCase):
    def test_home_resolves_per_language_prefix(self):
        for prefix in ("it", "de", "ar", "zh-hans"):
            res = self.client.get(f"/{prefix}/")
            self.assertEqual(res.status_code, 200, msg=prefix)
            self.assertIn(b"home", res.content)

    def test_object_detail_slug(self):
        res = self.client.get("/it/object/detail-item/")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"object:detail-item", res.content)

    def test_set_language_url_name(self):
        url = reverse("set_language")
        self.assertTrue(url.endswith("/"))
