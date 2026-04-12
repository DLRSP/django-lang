# Configuration (`lang.conf` and `APP_CONFIG`)

Runtime values are resolved in **`lang.conf`**: project settings first, then merges from **`settings.APP_CONFIG["lang"]`**, then **`lang.defaults`**.

You do **not** need to import `lang.defaults` in `settings.py`.

## Optional top-level settings

Examples (all optional):

- `LANGUAGE_HREFLANG_MAP` — Django language code → BCP 47 hreflang value
- `HREFLANG_DEFAULT_LANGUAGE` — drives `x-default` in `hreflang.html` when set
- `LANGUAGE_WIKIPEDIA_SAMEAS` — map for JSON-LD / `sameAs`
- `OG_LOCALE_BY_LANGUAGE` — Open Graph locale strings (e.g. `it_IT`)
- `LANGUAGE_FLAG_MAP` — Django code → region code for `emoji-country-flag`

## `APP_CONFIG` example

Typical site override for `x-default`:

```python
APP_CONFIG = {
    "lang": {
        "HREFLANG_DEFAULT_LANGUAGE": "it",
    },
}
```

Partial dicts are **merged** onto package defaults for the maps above.
