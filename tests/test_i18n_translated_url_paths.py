"""
Scope: gettext_lazy URL path segments under i18n_patterns (per-language path prefix).

Covers sites that use translated URL patterns (e.g. with django-modeltranslation) or
manual gettext_lazy paths; ``translate_url`` / ``django.urls.translate_url`` must link
across languages for the same logical route name.

Requires compiled ``tests/locale/*/LC_MESSAGES/django.mo`` (run ``msgfmt`` after editing .po).
"""

from django.template import RequestContext, Template
from django.test import TestCase
from django.urls import reverse
from django.utils import translation


class TranslatedPathReverseTests(TestCase):
    def test_item_detail_path_differs_by_active_language(self):
        with translation.override("en"):
            self.assertEqual(
                reverse("item-detail", kwargs={"slug": "abc"}),
                "/en/item/abc/",
            )
        with translation.override("it"):
            self.assertEqual(
                reverse("item-detail", kwargs={"slug": "abc"}),
                "/it/oggetto/abc/",
            )
        with translation.override("de"):
            self.assertEqual(
                reverse("item-detail", kwargs={"slug": "abc"}),
                "/de/artikel/abc/",
            )

    def test_item_detail_pages_respond_200(self):
        paths = (
            ("/en/item/x/", "en"),
            ("/it/oggetto/x/", "it"),
            ("/de/artikel/x/", "de"),
        )
        for path, lang in paths:
            with translation.override(lang):
                res = self.client.get(path)
                self.assertEqual(res.status_code, 200, msg=path)
                self.assertIn(b"object:x", res.content)


class TranslateUrlAcrossTranslatedPathsTests(TestCase):
    """translate_url must target the correct translated segment for the same view."""

    def test_from_italian_item_to_german_item_url(self):
        translation.activate("it")
        try:
            response = self.client.get("/it/oggetto/shared-slug/")
            self.assertEqual(response.status_code, 200)
            request = response.wsgi_request
            tpl = Template("{% load urls %}{% translate_url 'de' %}")
            out = tpl.render(RequestContext(request, {}))
        finally:
            translation.deactivate()
        self.assertIn("http://testserver/de/artikel/shared-slug/", out)

    def test_from_english_item_to_italian_item_url(self):
        translation.activate("en")
        try:
            response = self.client.get("/en/item/shared-slug/")
            self.assertEqual(response.status_code, 200)
            request = response.wsgi_request
            tpl = Template("{% load urls %}{% translate_url 'it' %}")
            out = tpl.render(RequestContext(request, {}))
        finally:
            translation.deactivate()
        self.assertIn("http://testserver/it/oggetto/shared-slug/", out)
