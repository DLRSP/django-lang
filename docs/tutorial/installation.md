# Installation & setup

## pip

```shell
pip install django-lang
```

## `INSTALLED_APPS` and `TEMPLATES`

See the [home page](../index.md) for the minimal `INSTALLED_APPS` and `TEMPLATES` snippet.

Optional context processor for the packaged language form (`redirect_to` / `next`):

```python
"lang.context_processors.language_switcher_next",
```

## Locale middleware

`LocaleMiddleware` must be enabled:

```python
MIDDLEWARE = (
    # ...
    "django.middleware.locale.LocaleMiddleware",
    # ...
)
```

## Base template: CSS

```html
<head>
    ...
    <link rel="stylesheet" type="text/css" href="{% static 'lang/css/nav-link.css' %}">
    ...
</head>
```

## Base template: language meta and hreflang

```html
<head>
    ...
    <meta name="language" content="{{ LANGUAGE_CODE }}" />
    {% include "hreflang.html" %}
    ...
</head>
```

## Nav: language switcher

```html
<nav class="navbar">
    ...
    <ul class="nav navbar-nav">
        {% include "lang/nav-link.html" %}
    </ul>
    ...
</nav>
```

## Demo project

```shell
git clone --depth=50 --branch=django-lang https://github.com/DLRSP/example.git
cd example
python manage.py runserver
```

Open <http://127.0.0.1:8000>.
