"""
Typical consumer-site patterns for django-lang:

- Root layout: ``{% include "hreflang.html" %}`` with
  ``lang.context_processors.from_settings`` and optional SEO override of
  ``DEFAULT_LANGUAGE_CODE`` for ``x-default``.
- Language switcher: ``lang/nav-link.html`` (options only, no ``<li>`` inside ``<select>``),
  optional ``lang/nav-link-standalone.html``,
  ``redirect_to`` for ``set_language`` ``next``.
- ``translate_url`` on real paths: query strings, ``JavaScriptCatalog`` (``jsi18n``).
"""

from django.conf import settings
from django.template import RequestContext, Template
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import translation

from lang.utils import get_hreflang_code

from tests.hreflang_html import parse_alternate_links


class HreflangContextProcessorIntegrationTests(TestCase):
    """hreflang.html without passing DEFAULT_LANGUAGE_CODE from the view."""

    def test_hreflang_context_only_uses_hreflang_default_for_x_default(self):
        """With HREFLANG_DEFAULT_LANGUAGE=it, x-default targets that locale."""
        res = self.client.get("/it/demo/hreflang-context/")
        self.assertEqual(res.status_code, 200)
        content = res.content.decode()
        self.assertIn('hreflang="x-default"', content)
        self.assertIn("/it/demo/hreflang-context/", content)
        pairs = parse_alternate_links(content)
        self.assertEqual(len(pairs), len(settings.LANGUAGES) + 1)
        hreflangs = {h for h, _ in pairs}
        self.assertEqual(hreflangs, {get_hreflang_code(c) for c, _ in settings.LANGUAGES} | {"x-default"})
        x_default_url = next(url for hl, url in pairs if hl == "x-default")
        self.assertTrue(x_default_url.startswith("http"))
        self.assertIn("/it/demo/hreflang-context/", x_default_url)

    @override_settings(HREFLANG_DEFAULT_LANGUAGE="")
    def test_hreflang_context_only_falls_back_to_language_code_when_no_seo_default(
        self,
    ):
        """If HREFLANG_DEFAULT_LANGUAGE is unset/empty, x-default uses LANGUAGE_CODE."""
        res = self.client.get("/it/demo/hreflang-context/")
        self.assertEqual(res.status_code, 200)
        content = res.content.decode()
        self.assertIn('hreflang="x-default"', content)
        self.assertIn("/en/demo/hreflang-context/", content)


class LanguageSwitcherMarkupTests(TestCase):
    """Packaged nav-link vs minimal markup variant."""

    def test_minimal_markup_nav_renders_form_and_languages(self):
        res = self.client.get("/it/demo/nav-link-minimal/")
        self.assertEqual(res.status_code, 200)
        content = res.content.decode()
        self.assertIn('id="language-switcher"', content)
        self.assertIn(reverse("set_language"), content)
        self.assertIn('name="next"', content)
        self.assertIn("/it/demo/nav-link-minimal/", content)
        self.assertIn('value="it"', content)
        select_body = content.split("<select")[1].split("</select>")[0]
        self.assertNotIn("<li ", select_body)

    def test_nav_without_redirect_to_renders_empty_next(self):
        """Missing ``redirect_to`` yields empty hidden next (still valid form)."""
        res = self.client.get("/it/demo/nav-link-no-redirect/")
        self.assertEqual(res.status_code, 200)
        self.assertRegex(
            res.content.decode(),
            r'<input[^>]+name="next"[^>]+value=""',
        )

    def test_nav_link_standalone_renders_second_id_and_wrapper_class(self):
        res = self.client.get("/it/demo/nav-link-standalone/")
        self.assertEqual(res.status_code, 200)
        content = res.content.decode()
        self.assertIn('id="language-switcher-standalone"', content)
        self.assertIn('class="lang-switcher-standalone"', content)
        self.assertIn(reverse("set_language"), content)


class BaseTemplateLoadChainTests(TestCase):
    """Many sites load ``i18n`` and ``urls`` before including hreflang partials."""

    def test_hreflang_include_after_load_i18n_and_urls(self):
        tpl = Template('{% load i18n urls %}{% include "hreflang.html" %}')
        translation.activate("it")
        self.addCleanup(translation.deactivate)
        request = self.client.get("/it/object/chain-test/").wsgi_request
        html = tpl.render(RequestContext(request))
        self.assertIn('rel="alternate"', html)
        self.assertIn("hreflang", html)


class TranslateUrlSitePathsTests(TestCase):
    def test_translate_url_preserves_query_string(self):
        translation.activate("it")
        try:
            response = self.client.get(
                "/it/object/qs-test/?utm_source=demo&utm_medium=test"
            )
            self.assertEqual(response.status_code, 200)
            request = response.wsgi_request
            tpl = Template("{% load urls %}{% translate_url 'de' %}")
            out = tpl.render(RequestContext(request, {}))
        finally:
            translation.deactivate()
        self.assertIn("utm_source=demo", out)
        self.assertIn("utm_medium=test", out)
        self.assertIn("/de/object/qs-test/", out)

    def test_translate_url_from_javascript_catalog_page(self):
        """JavaScriptCatalog is often mounted under the language prefix."""
        translation.activate("it")
        try:
            response = self.client.get("/it/jsi18n/")
            self.assertEqual(response.status_code, 200)
            request = response.wsgi_request
            tpl = Template("{% load urls %}{% translate_url 'de' %}")
            out = tpl.render(RequestContext(request, {}))
        finally:
            translation.deactivate()
        self.assertIn("http://testserver/de/jsi18n/", out)
