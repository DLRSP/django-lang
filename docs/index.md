# django-lang

Helpers for multilingual Django sites: **hreflang** links, a packaged **language switcher** (`nav-link` templates), optional **SEO / Open Graph** context, flag emoji mapping, and an optional **middleware** for `set_language` when URLs use translated path segments (`gettext_lazy`).

---

## Requirements

- Python 3.8+
- Django 3.2+ (see package metadata on PyPI for tested releases)

---

## Installation

```shell
pip install django-lang
```

Add the app:

```python
INSTALLED_APPS = [
    # ...
    "lang",
    # ...
]
```

Enable context processors (minimal stack):

```python
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [...],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                "lang.context_processors.from_settings",
                "lang.context_processors.seo_i18n",
                # optional: "lang.context_processors.language_switcher_next",
            ],
        },
    },
]
```

Ensure **`django.middleware.locale.LocaleMiddleware`** is in `MIDDLEWARE` and that you use **`i18n_patterns`** (or equivalent) for prefixed language URLs.

---

## Next steps

- [Installation & setup](tutorial/installation.md) — templates, static files, demo project
- [Configuration (APP_CONFIG)](tutorial/configuration.md) — hreflang, flags, overrides
- [Templates & nav](tutorial/templates.md) — `hreflang.html`, switcher, standalone layout
- [Set language middleware](tutorial/set_language_middleware.md) — optional fix for `gettext_lazy` URL paths

MkDocs sources live under `docs/`. To build locally: [Contributing](community/contributing.md).
