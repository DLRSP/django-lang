"""Views used only by the django-lang test URLconf."""

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(
        request,
        "simple.html",
        {"title": "home"},
    )


def object_detail(request, slug):
    return render(
        request,
        "simple.html",
        {"title": f"object:{slug}"},
    )


def object_detail_response_with_url(request, slug):
    """
    Returns an HttpResponse carrying a ``url`` attribute.

    Exercises ``translate_url`` when ``match.func`` returns a response object
    with ``.url`` (path-only), instead of using ``reverse`` +
    ``django.urls.translate_url`` on the HttpResponse.
    """
    resp = HttpResponse("url-attr-branch")
    resp.url = f"/de/object-url-attr/{slug}/"
    return resp


def hreflang_demo(request):
    """Renders ``hreflang.html`` (x-default via DEFAULT_LANGUAGE_CODE)."""
    return render(
        request,
        "hreflang_demo.html",
        {
            "DEFAULT_LANGUAGE_CODE": getattr(
                settings, "HREFLANG_DEFAULT_LANGUAGE", "it"
            ),
        },
    )


def nav_link_demo(request):
    """Renders packaged nav-link.html (redirect_to = current path for set_language next)."""
    return render(
        request,
        "nav_link_demo.html",
        {"redirect_to": request.get_full_path()},
    )


def hreflang_context_only(request):
    """
    ``hreflang.html`` with no view-supplied DEFAULT_LANGUAGE_CODE — only context processors
    (from_settings + seo_i18n), as in a typical site root template.
    """
    return render(request, "hreflang_only.html")


def nav_link_minimal_markup_demo(request):
    """Minimal language switcher: no aria-label, no ``<li>`` inside ``<select>``."""
    return render(
        request,
        "nav_link_minimal_markup.html",
        {"redirect_to": request.get_full_path()},
    )


def nav_link_no_redirect_demo(request):
    """Include language switcher without ``redirect_to`` in context (empty ``next``)."""
    return render(request, "nav_link_minimal_markup.html", {})


def nav_link_standalone_demo(request):
    """Packaged ``lang/nav-link-standalone.html`` (second switcher id)."""
    return render(
        request,
        "nav_link_standalone_demo.html",
        {"redirect_to": request.get_full_path()},
    )
