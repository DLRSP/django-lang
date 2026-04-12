# Templates & navigation

## Packaged templates

| Template | Role |
| -------- | ---- |
| `hreflang.html` | `<link rel="alternate" hreflang="…">` for the current view |
| `lang/nav-link.html` | Language `<select>` posting to `set_language`; optional context: `lang_switcher_id`, `lang_switcher_extra_class` |
| `lang/nav-link-standalone.html` | Extra switcher beside the mobile menu toggle (small viewports / PWA) |

## Standalone switcher (small screens)

`nav-link-standalone.css` places a second switcher near the menu toggle (below the `lg` breakpoint) and hides the duplicate inside the collapsed drawer. Optional `display-standalone-class.js` adds `display-standalone` on `<html>` for installed web apps.

1. Add the context processor if you use the packaged form without passing `redirect_to` per view:

    ```python
    "lang.context_processors.language_switcher_next",
    ```

2. After `nav-link.css` in `<head>`:

    ```html
    <link rel="stylesheet" href="{% static 'lang/css/nav-link-standalone.css' %}">
    <script src="{% static 'lang/js/display-standalone-class.js' %}"></script>
    ```

3. Next to the mobile menu control:

    ```html
    {% include "lang/nav-link-standalone.html" %}
    ```

## `translate_url` template tag

The package ships a `translate_url` tag (see package templatetags) for links between language versions; use it where you need explicit alternate URLs in templates.
