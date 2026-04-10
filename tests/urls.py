"""URLconf for django-lang tests (i18n_patterns + set_language, typical multi-language site layout)."""

from django.conf.urls.i18n import i18n_patterns
from django.urls import path
from django.utils.translation import gettext_lazy as _
from django.views.i18n import JavaScriptCatalog, set_language

from tests import views

urlpatterns = [
    path("i18n/setlang/", set_language, name="set_language"),
]

def _object_detail_dispatch(request, slug):
    """Resolve ``views.object_detail`` at call time so tests can patch it with ``wraps``."""
    return views.object_detail(request, slug)


urlpatterns += i18n_patterns(
    path("", views.home, name="test-home"),
    path("object/<slug:slug>/", _object_detail_dispatch, name="object-detail"),
    path(
        "object-url-attr/<slug:slug>/",
        views.object_detail_response_with_url,
        name="object-detail-url-attr",
    ),
    # Translated path segment (see tests/locale/it/LC_MESSAGES/django.po).
    path(_("item/<slug:slug>/"), _object_detail_dispatch, name="item-detail"),
    path("demo/hreflang/", views.hreflang_demo, name="hreflang-demo"),
    path(
        "demo/hreflang-context/",
        views.hreflang_context_only,
        name="hreflang-context-only",
    ),
    path("demo/nav-link/", views.nav_link_demo, name="nav-link-demo"),
    path(
        "demo/nav-link-minimal/",
        views.nav_link_minimal_markup_demo,
        name="nav-link-minimal-demo",
    ),
    path(
        "demo/nav-link-no-redirect/",
        views.nav_link_no_redirect_demo,
        name="nav-link-no-redirect-demo",
    ),
    path(
        "demo/nav-link-standalone/",
        views.nav_link_standalone_demo,
        name="nav-link-standalone-demo",
    ),
    path("jsi18n/", JavaScriptCatalog.as_view(), name="javascript-catalog"),
)
