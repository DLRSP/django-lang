# !!! Remove this section !!!
1. Create empty Git repository with your preferred name: example `django-my-new-pkg-name`
2. Checkout local copy of this new **empty** repository
3. Copy all the contents of this repository inside the **new cloned empty repository**
4. Delete the directory **src\django_pkg.egg-info**
5. Rename the directory inside **src** from `PACKAGE_NAME` to `my_new_pkg_src_location`
6. Massive **replace** with match case the string `PACKAGE_NAME` with your src location `my_new_pkg_src_location`
7. Massive **replace** the string `django-pkg` with your new package's name `django-my-new-pkg-name`
8. **Edit** the `setup.cfg` file for the needed  app's `description` attribute
9. **Edit** the `tests/settings.py` file for the needed configuration to test your app
10. **Rename and edit** the `tests/test_fake.py` file for the needed application's tests
11. Copy or create all source's files of the app inside the **src/my_new_pkg_src_location**
12. Install python's requirements `pip install -r requirements/dev.in`
13. Install python's requirements `pip install -r requirements/requirements.in`
14. Install python's package `pip install .` to test the package's local version
15. Execute `python runtests.py` and validate all tests are passed (if any error is present, the automatic workflow on tag will fail)
16. Edit the file `README.md` removing these notes and change needed information
17. Edit docs ...
18. Install python requirements `pip install -r requirements/docs.in`
19. Add files as first commit `git add .github requirements/*`
20. Commits `git commit -m "Initial commit"`
21. Push to remote git the current repository's local initial's commit `git push`
21. Inside Git repository's workflows, manually execute the first run of **Upgrade dependencies** workflow and wait the **Success** finish
22. Inside Git repository's workflows, wait the **Pull request** CI workflow's complete and its status is **Merged** 
23. Pull to local git copy the workflow's generated requirements
24. Add all others local files as first commit `git add .`
25. Execute `bump-my-verion` to upgrade the initial 0.0.0 version
26. Execute `python setup.py sdist bdist_wheel` to build the project
27. Execute `twine upload dist/*` to upload the built files
28. Inside PyPi repository, section *Account Settings -> API tokens*, **generate** new API key with the only scope of project
29. Inside Git repository's settings, section *General*, **enable** the `Allow auto-merge` and `Automatically delete head branches`
30. Inside Git repository's settings, section *Access*, **add access** to be able to execute workflows (as team member's or bot-user collaborator)
31. Inside Git repository's settings, section *Security*, **add security repository secret** named `PYPI_API_TOKEN` to be able to upload packages inside PyPi's repository
32. Push to remote git the current repository's local commits and tags


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
3. Modify your project's base template `base.html` to include language's switcher styles:
```html
<head>
    ...
    <link rel="stylesheet" type="text/css" href="{% static 'lang/css/nav-link.css' %}">
    ...
</head>
```
4. Modify your project's nav template `nav.html` to include language's switcher:
```html
<ul class="nav navbar-nav">
    {% include "lang/nav-link.html" %}
</ul>
```
5. Modify your project's base template `base.html` to include language's templatetags `urls`:
```html
{% load i18n urls %}
```
6. Modify your project's base template `base.html` to include attributes using `translate_url` template's tag:
```html
<head>
    ...
    <!-- hreflang -->
    <meta name="language" content="{{ LANGUAGE_CODE }}" />
    {% get_available_languages as LANGUAGES %}
    {% for language_code, language_name in LANGUAGES %}
    <link rel="alternate" hreflang="{{ language_code }}" href="{% translate_url language_code %}" />
    {% endfor %}
    <link rel="alternate" href="{% translate_url 'it' %}" hreflang="x-default" />
    ...
</head>
```

## Run Example Project

```shell
git clone --depth=50 --branch=django-lang https://github.com/DLRSP/example.git DLRSP/example
cd DLRSP/example
python manage.py runserver
```

Now browser the app @ http://127.0.0.1:8000
