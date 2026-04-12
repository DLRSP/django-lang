# django-lang [![PyPi license](https://img.shields.io/pypi/l/django-lang.svg)](https://pypi.python.org/pypi/django-lang)

[![PyPi status](https://img.shields.io/pypi/status/django-lang.svg)](https://pypi.python.org/pypi/django-lang)
[![PyPi version](https://img.shields.io/pypi/v/django-lang.svg)](https://pypi.python.org/pypi/django-lang)
[![PyPi python version](https://img.shields.io/pypi/pyversions/django-lang.svg)](https://pypi.python.org/pypi/django-lang)
[![PyPi downloads](https://img.shields.io/pypi/dm/django-lang.svg)](https://pypi.python.org/pypi/django-lang)
[![PyPi downloads](https://img.shields.io/pypi/dw/django-lang.svg)](https://pypi.python.org/pypi/django-lang)
[![PyPi downloads](https://img.shields.io/pypi/dd/django-lang.svg)](https://pypi.python.org/pypi/django-lang)

## GitHub ![GitHub release](https://img.shields.io/github/tag/DLRSP/django-lang.svg) ![GitHub release](https://img.shields.io/github/release/DLRSP/django-lang.svg)

## Test [![codecov.io](https://codecov.io/github/DLRSP/django-lang/coverage.svg?branch=main)](https://codecov.io/github/DLRSP/django-lang?branch=main) [![pre-commit.ci status](https://results.pre-commit.ci/badge/github/DLRSP/django-lang/main.svg)](https://results.pre-commit.ci/latest/github/DLRSP/django-lang/main) [![gitthub.com](https://github.com/DLRSP/django-lang/actions/workflows/ci.yaml/badge.svg)](https://github.com/DLRSP/django-lang/actions/workflows/ci.yaml)

## Check Demo Project
* Check the demo repo on [GitHub](https://github.com/DLRSP/example/tree/django-lang)

## Requirements
-   Python 3.8+ supported.
-   Django 3.2+ supported.

## Setup
1. Install from **pip**:
    ```shell
    pip install django-lang
    ```
2. Modify `settings.py` by adding the app to `INSTALLED_APPS`:
    ```python
    INSTALLED_APPS = [
        # ...
        "lang",
        # ...
    ]
    ```
3. Modify `settings.py` by adding the app to `INSTALLED_APPS`:
    ``` python title="settings.py" hl_lines="12"
    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [os.path.join(PROJECT_DIR, "templates")],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                    "lang.context_processors.from_settings",
                    "lang.context_processors.seo_i18n",
                ],
            },
        },
    ]
    ```

    Optional: ``lang.context_processors.language_switcher_next`` (fills ``redirect_to`` for the packaged language form).

### Optional: ``SetLanguageNextPathMiddleware``

Only needed if you use **translated URL segments** (``gettext_lazy`` under ``i18n_patterns``) and see language switches that POST to ``set_language`` but stay on the wrong prefix. Short how-to: [docs/set_language_middleware.md](docs/set_language_middleware.md).

4. Modify your project's base template `base.html` to include language's switcher styles:
    ```html
    <head>
        ...
        <link rel="stylesheet" type="text/css" href="{% static 'lang/css/nav-link.css' %}">
        ...
    </head>
    ```
5. Modify your project's base template `base.html` to include attributes using `translate_url` template's tag:
    ```html
    <head>
        ...
        <meta name="language" content="{{ LANGUAGE_CODE }}" />
        {% include "hreflang.html" %}
        ...
    </head>
    ```
6. Modify your project's nav template `nav.html` to include language's switcher:
    ```html
    <nav class="navbar">
        ...
        <ul class="nav navbar-nav">
            {% include "lang/nav-link.html" %}
        </ul>
        ...
    </nav>
    ```

### Configuration: ``lang.conf`` and ``APP_CONFIG``

Built-in maps live in ``lang.defaults``. At runtime, :mod:`lang.conf` resolves values **lazily**:

1. Top-level Django settings (``LANGUAGE_HREFLANG_MAP``, ``LANGUAGE_WIKIPEDIA_SAMEAS``, ``OG_LOCALE_BY_LANGUAGE``, ``HREFLANG_DEFAULT_LANGUAGE``, ``LANGUAGE_FLAG_MAP``), if set.
2. Partial dicts under ``settings.APP_CONFIG["lang"]`` merged onto the package defaults (for the three ``LANGUAGE_*`` / ``OG_*`` maps and flag overrides).
3. Otherwise the content of ``lang.defaults``.

You do **not** need to import ``lang.defaults`` from ``settings.py``. Typical site-only override for ``x-default``::

    APP_CONFIG = {
        "lang": {
            "HREFLANG_DEFAULT_LANGUAGE": "it",
        },
    }

Or use the usual flat settings (full replacement for the dict keys, or ``HREFLANG_DEFAULT_LANGUAGE`` at top level) if you prefer.

### Optional: language control beside the hamburger on **small viewports**

``nav-link-standalone.css`` shows the extra switcher next to the menu toggle below the ``lg`` breakpoint (~992px) and hides the duplicate inside the collapsed drawer. Optional script ``display-standalone-class.js`` only adds class ``display-standalone`` on ``<html>`` for installed web apps; layout no longer depends on it.

1. In `settings.py`, add the optional context processor so `redirect_to` is filled for `set_language`’s `next` (unless you pass `redirect_to` from each view):
    ```python
    "lang.context_processors.language_switcher_next",
    ```
2. In the base layout `<head>`, after `nav-link.css`, add:
    ```html
    <link rel="stylesheet" href="{% static 'lang/css/nav-link-standalone.css' %}">
    <script src="{% static 'lang/js/display-standalone-class.js' %}"></script>
    ```
3. Next to your mobile menu button, include:
    ```html
    {% include "lang/nav-link-standalone.html" %}
    ```

Packaged templates:

- ``hreflang.html`` (app template root) — ``<link rel="alternate" hreflang="…">`` for the current view.
- ``lang/nav-link.html`` — language ``<select>`` (optional context: ``lang_switcher_id``, ``lang_switcher_extra_class``).
- ``lang/nav-link-standalone.html`` — duplicate switcher beside the mobile toggle (small viewports / PWA).


## Run Example Project

```shell
git clone --depth=50 --branch=django-lang https://github.com/DLRSP/example.git DLRSP/example
cd DLRSP/example
python manage.py runserver
```

Now browser the app @ http://127.0.0.1:8000

## References

- [brainstorm.it](https://brainstorm.it/snippets/django-language-switching/) - Language's switching
- [hakibenita.com](https://hakibenita.com/django-multi-language-site-hreflang) - Url's translation for "hreflang" html's attributes
