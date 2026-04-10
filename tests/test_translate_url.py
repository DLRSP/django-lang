"""
Scope: ``translate_url`` template tag (per-language URLs, session cache, fallbacks).

Regression contract:
- ``TranslateUrlCurrentBehaviorTests`` documents current behavior (including the
  extra resolved-view invocation). Update or remove after an intentional refactor.
- ``TranslateUrlPlannedBehaviorTests`` is ``xfail`` until ``translate_url`` uses
  ``reverse`` + ``django.urls.translate_url`` only (no ``match.func``).

Related: translated URL segments — ``test_i18n_translated_url_paths.py``;
query string / jsi18n — ``test_site_integration.py``.
"""

import pytest
from unittest.mock import patch

from django.contrib.sessions.middleware import SessionMiddleware
from django.template import RequestContext, Template
from django.test import RequestFactory, TestCase
from django.urls import translate_url as django_translate_url
from django.utils import translation

import lang.templatetags.urls as translate_url_tag
from tests import views


class TranslateUrlTagTests(TestCase):
    def _render_translate_url(self, path, target_lang, activate_lang=None, **client_get_kw):
        if activate_lang:
            translation.activate(activate_lang)
        try:
            response = self.client.get(path, **client_get_kw)
            self.assertEqual(
                response.status_code,
                200,
                msg=f"Failed to load {path}: {response.status_code}",
            )
            request = response.wsgi_request
            tpl = Template("{% load urls %}{% translate_url target %}")
            return tpl.render(
                RequestContext(
                    request,
                    {"target": target_lang},
                )
            )
        finally:
            if activate_lang:
                translation.deactivate()

    def test_translates_object_path_to_other_language(self):
        out = self._render_translate_url(
            "/it/object/sample-slug/",
            "de",
            activate_lang="it",
        )
        self.assertIn("http://testserver/de/object/sample-slug/", out)

    def test_translates_home_prefix(self):
        out = self._render_translate_url("/en/", "it", activate_lang="en")
        self.assertIn("http://testserver/it/", out)

    def test_session_caches_translated_url_per_language(self):
        path = "/fr/object/cache-me/"
        translation.activate("fr")
        try:
            response = self.client.get(path)
            request = response.wsgi_request
            tpl = Template("{% load urls %}{% translate_url 'es' %}")
            first = tpl.render(RequestContext(request, {}))
            second = tpl.render(RequestContext(request, {}))
            self.assertEqual(first, second)
            self.assertIn("/es/object/cache-me/", first)
        finally:
            translation.deactivate()

    def test_session_cache_isolated_per_target_language(self):
        """Each target language has its own ``translated_url_*`` session slot."""
        with patch.object(views, "object_detail", wraps=views.object_detail) as spy:
            response = self.client.get("/it/object/cache-by-lang/")
            self.assertEqual(spy.call_count, 1)
            request = response.wsgi_request
            translation.activate("it")
            try:
                de_out = Template("{% load urls %}{% translate_url 'de' %}").render(
                    RequestContext(request, {})
                )
                fr_out = Template("{% load urls %}{% translate_url 'fr' %}").render(
                    RequestContext(request, {})
                )
                de_again = Template("{% load urls %}{% translate_url 'de' %}").render(
                    RequestContext(request, {})
                )
            finally:
                translation.deactivate()
        self.assertIn("/de/object/cache-by-lang/", de_out)
        self.assertIn("/fr/object/cache-by-lang/", fr_out)
        self.assertEqual(de_out, de_again)
        # GET + first translate_url per lang runs the view; second de hits cache.
        self.assertEqual(
            spy.call_count,
            3,
            msg="Expected one view run per first translate_url per target language",
        )

    def test_uses_https_scheme_when_request_is_secure(self):
        out = self._render_translate_url(
            "/it/object/https-obj/",
            "de",
            activate_lang="it",
            secure=True,
        )
        self.assertTrue(
            out.startswith("https://"),
            msg=f"Expected absolute https URL, got {out!r}",
        )
        self.assertIn("/de/object/https-obj/", out)


class TranslateUrlResponseUrlAttributeTests(TestCase):
    """``match.func`` returns a response with a ``url`` path."""

    def test_uses_response_url_path_when_present(self):
        translation.activate("it")
        try:
            response = self.client.get("/it/object-url-attr/special/")
            self.assertEqual(response.status_code, 200)
            request = response.wsgi_request
            out = Template("{% load urls %}{% translate_url 'de' %}").render(
                RequestContext(request, {})
            )
        finally:
            translation.deactivate()
        self.assertIn("http://testserver/de/object-url-attr/special/", out)


class TranslateUrlSessionReentryTests(TestCase):
    """``translated_iter_*`` plus cached URL short-circuits re-entry."""

    def test_returns_cached_url_when_iteration_flag_is_set(self):
        rf = RequestFactory()
        request = rf.get("/it/object/guarded/", HTTP_HOST="testserver")
        SessionMiddleware(lambda r: None).process_request(request)
        request.session.save()
        seeded = "http://testserver/seeded-de-only/"
        setattr(request.session, "translated_iter_de", 1)
        setattr(request.session, "translated_url_de", seeded)
        translation.activate("it")
        try:
            with patch.object(views, "object_detail", wraps=views.object_detail) as spy:
                out = Template("{% load urls %}{% translate_url 'de' %}").render(
                    RequestContext(request, {})
                )
        finally:
            translation.deactivate()
        self.assertEqual(out, seeded)
        self.assertEqual(
            spy.call_count,
            0,
            msg="Pre-set iter/url must skip resolving and calling the view",
        )


class TranslateUrlReverseFailureTests(TestCase):
    """If ``reverse`` raises in the resolve branch, fall back to django ``translate_url``."""

    def test_fallback_when_reverse_raises(self):
        translation.activate("it")
        try:
            response = self.client.get("/it/object/reverse-fail/")
            self.assertEqual(response.status_code, 200)
            request = response.wsgi_request
            absolute = request.build_absolute_uri()
            expected = django_translate_url(absolute, "de")
            with patch.object(
                translate_url_tag,
                "reverse",
                side_effect=RuntimeError("reverse unavailable"),
            ):
                out = Template("{% load urls %}{% translate_url 'de' %}").render(
                    RequestContext(request, {})
                )
        finally:
            translation.deactivate()
        self.assertEqual(out, expected)
        self.assertIn("/de/object/reverse-fail/", out)


class TranslateUrlEdgeCaseTests(TestCase):
    """When ``resolve()`` fails (unknown path under prefix)."""

    def test_unknown_path_still_returns_absolute_url(self):
        rf = RequestFactory()
        request = rf.get("/it/unknown-404-path/", HTTP_HOST="testserver")
        SessionMiddleware(lambda r: None).process_request(request)
        request.session.save()
        translation.activate("it")
        self.addCleanup(translation.deactivate)
        tpl = Template("{% load urls %}{% translate_url 'de' %}")
        out = tpl.render(RequestContext(request, {}))
        self.assertTrue(out.startswith("http://testserver"))
        self.assertEqual(
            out,
            django_translate_url(request.build_absolute_uri(), "de"),
        )


class TranslateUrlCurrentBehaviorTests(TestCase):
    """
    Baseline for the current implementation.

    After refactoring ``translate_url`` to avoid ``match.func``, remove or replace
    (the view should run only for the page GET).
    """

    def test_translate_url_re_invokes_resolved_view_once(self):
        with patch.object(views, "object_detail", wraps=views.object_detail) as spy:
            response = self.client.get("/it/object/slug-baseline/")
            self.assertEqual(spy.call_count, 1)
            translation.activate("it")
            try:
                Template("{% load urls %}{% translate_url 'de' %}").render(
                    RequestContext(response.wsgi_request, {})
                )
            finally:
                translation.deactivate()
        self.assertEqual(
            spy.call_count,
            2,
            msg=(
                "Current implementation: translate_url calls match.func again. "
                "After refactor to reverse-only, expect 1 and remove this test."
            ),
        )


class TranslateUrlPlannedBehaviorTests(TestCase):
    """Target behavior after ``translate_url`` refactor (no view execution)."""

    @pytest.mark.xfail(
        reason=(
            "translate_url still invokes match.func; should use reverse + "
            "django.urls.translate_url only (no duplicate view runs / side effects)"
        ),
        strict=False,
    )
    def test_translate_url_does_not_call_object_detail_again(self):
        with patch.object(views, "object_detail", wraps=views.object_detail) as spy:
            response = self.client.get("/it/object/slug-a/")
            self.assertEqual(spy.call_count, 1)
            request = response.wsgi_request
            translation.activate("it")
            try:
                Template("{% load urls %}{% translate_url 'de' %}").render(
                    RequestContext(request, {})
                )
            finally:
                translation.deactivate()
            self.assertEqual(
                spy.call_count,
                1,
                "translate_url must not invoke object_detail; only the page GET should",
            )
