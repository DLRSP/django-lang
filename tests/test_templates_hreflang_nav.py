"""
Scope: rendering ``hreflang.html`` and ``lang/nav-link*.html`` via demo views.

Out of scope: JavaScriptCatalog content.
"""

from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from lang.utils import get_hreflang_code

from tests.hreflang_html import parse_alternate_links


class HreflangTemplateTests(TestCase):
    def test_hreflang_demo_lists_all_languages_and_x_default(self):
        res = self.client.get("/it/demo/hreflang/")
        self.assertEqual(res.status_code, 200)
        content = res.content.decode()
        for code, _ in settings.LANGUAGES:
            hreflang = get_hreflang_code(code)
            self.assertIn(f'hreflang="{hreflang}"', content)
        self.assertIn('hreflang="x-default"', content)
        self.assertIn("/it/demo/hreflang/", content)

    def test_zh_hans_uses_bcp47_mapping_in_hreflang_attribute(self):
        """LANGUAGE_HREFLANG_MAP maps zh-hans → zh-Hans in the link tag."""
        res = self.client.get("/it/demo/hreflang/")
        self.assertEqual(res.status_code, 200)
        content = res.content.decode()
        self.assertIn('hreflang="zh-Hans"', content)
        self.assertNotIn('hreflang="zh-hans"', content)


class HreflangAlternateLinkOutputTests(TestCase):
    """
    Structured checks for ``<link rel="alternate" hreflang="…" href="…">`` as required
    for multilingual SEO (one entry per locale + ``x-default``).
    """

    def test_alternate_link_count_matches_languages_plus_x_default(self):
        res = self.client.get("/it/demo/hreflang/")
        self.assertEqual(res.status_code, 200)
        pairs = parse_alternate_links(res.content.decode())
        expected = len(settings.LANGUAGES) + 1  # x-default
        self.assertEqual(
            len(pairs),
            expected,
            msg=f"Expected {expected} alternate links, got {len(pairs)}: {pairs!r}",
        )

    def test_each_alternate_has_absolute_http_href(self):
        res = self.client.get("/it/demo/hreflang/")
        pairs = parse_alternate_links(res.content.decode())
        self.assertGreater(len(pairs), 0)
        for hreflang_attr, href in pairs:
            with self.subTest(hreflang=hreflang_attr):
                self.assertTrue(
                    href.startswith("http://") or href.startswith("https://"),
                    msg=f"href must be absolute URI, got {href!r}",
                )

    def test_alternate_hrefs_use_https_when_request_is_secure(self):
        """``build_absolute_uri`` must reflect TLS (production behind HTTPS)."""
        res = self.client.get("/it/demo/hreflang/", secure=True)
        self.assertEqual(res.status_code, 200)
        pairs = parse_alternate_links(res.content.decode())
        self.assertGreater(len(pairs), 0)
        for hreflang_attr, href in pairs:
            with self.subTest(hreflang=hreflang_attr):
                self.assertTrue(
                    href.startswith("https://"),
                    msg=f"Expected https absolute href, got {href!r}",
                )

    def test_hreflang_values_match_bcp47_mapping_and_include_x_default(self):
        res = self.client.get("/it/demo/hreflang/")
        pairs = parse_alternate_links(res.content.decode())
        hreflangs = [h for h, _ in pairs]
        for code, _ in settings.LANGUAGES:
            self.assertIn(get_hreflang_code(code), hreflangs)
        self.assertIn("x-default", hreflangs)
        self.assertEqual(len(hreflangs), len(set(hreflangs)), "duplicate hreflang value")

    def test_x_default_href_targets_default_language_url(self):
        """Packaged demo sets DEFAULT_LANGUAGE_CODE to Italian for x-default."""
        res = self.client.get("/it/demo/hreflang/")
        pairs = parse_alternate_links(res.content.decode())
        by_h = dict(pairs)
        self.assertIn("x-default", by_h)
        self.assertIn("/it/demo/hreflang/", by_h["x-default"])

    def test_german_alternate_href_uses_german_prefix(self):
        pairs = parse_alternate_links(
            self.client.get("/it/demo/hreflang/").content.decode()
        )
        by_h = dict(pairs)
        de_tag = get_hreflang_code("de")
        self.assertIn(de_tag, by_h)
        self.assertIn("http://testserver/de/demo/hreflang/", by_h[de_tag])


class NavLinkTemplateTests(TestCase):
    def test_nav_link_renders_switcher_and_csrf(self):
        res = self.client.get("/it/demo/nav-link/")
        self.assertEqual(res.status_code, 200)
        content = res.content.decode()
        self.assertIn('id="language-switcher"', content)
        self.assertIn(reverse("set_language"), content)
        self.assertIn("csrfmiddlewaretoken", content)
        self.assertIn('name="language"', content)
        for code, _ in settings.LANGUAGES:
            self.assertIn(f'<option value="{code}"', content)
        select_body = content.split("<select")[1].split("</select>")[0]
        self.assertNotIn("<li ", select_body)
