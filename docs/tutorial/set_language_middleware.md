# Optional middleware: `SetLanguageNextPathMiddleware`

Some sites use **translated path segments** in `urls.py` (`gettext_lazy` / `_('segment/')`) inside `i18n_patterns`. Django’s `set_language` view calls `translate_url`, which runs `resolve()` using the **current thread language**. On POST to `/i18n/setlang/` there is no language prefix in the URL, so that language often comes from the `django_language` cookie (e.g. default `LANGUAGE_CODE`). If the cookie says `en` but `next` is an Italian-prefixed URL like `/it/…/`, `resolve` can fail and the redirect keeps the old path. The new cookie may be set, yet the next page still follows the URL prefix—so the switch looks broken.

This middleware runs **after** `LocaleMiddleware`. For POSTs to `set_language`, if `next` has an i18n prefix, it activates that language before the view runs so `translate_url` sees the same patterns as a normal request on that path.

**Not for:** fixing 500s, missing migrations, or broken DB state—those are separate.

## Enable

Put it immediately **after** `django.middleware.locale.LocaleMiddleware`:

```python
MIDDLEWARE = [
    # ...
    "django.middleware.locale.LocaleMiddleware",
    "lang.middleware.SetLanguageNextPathMiddleware",
    # ...
]
```

Regression coverage: `tests/test_set_language_translated_path_mismatch.py`.
