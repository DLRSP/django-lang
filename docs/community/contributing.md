# Contributing

## Issues and discussions

- **Bugs and features:** [GitHub issues](https://github.com/DLRSP/django-lang/issues).
- Search existing issues first; mention package version, Python, and Django.

## Development setup

Fork [django-lang](https://github.com/DLRSP/django-lang), clone your fork, then:

```shell
python -m venv env
source env/bin/activate
# Windows: env\Scripts\activate

pip install -e ".[testing]"
# Or install from a pinned requirements file if you use one in CI.

pre-commit install
```

## Tests

From the repository root (uses `tests.settings` via `pyproject.toml`):

```shell
pytest tests/
```

`msgfmt` is used in `tests/conftest.py` to compile `tests/locale` catalogs when available.

## Documentation

Sources are Markdown under `docs/`. Install MkDocs and the Material theme, then:

```shell
pip install mkdocs mkdocs-material pymdown-extensions mkdocs-git-revision-date-plugin
mkdocs serve
```

```shell
mkdocs build
```

## Pull requests

Open a PR from a branch (not `main`). Run tests before you push. New behavior should include or extend tests.

## Code of conduct

Stay polite and professional. For broader norms, see the [Django code of conduct](https://www.djangoproject.com/conduct/).
