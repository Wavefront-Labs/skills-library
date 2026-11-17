---
id: computing-software.software-engineering.python.docstrings-and-api-docs-with-sphinx
name: docstrings-and-api-docs-with-sphinx
category: computing-software
field: software-engineering
product: python
tags: [python, python-quality, docstrings, sphinx, mkdocstrings, autodoc, numpydoc, api-documentation]
level: practitioner
status: verified
description: "Write useful docstrings (Google/NumPy style) and generate API docs with Sphinx autodoc or mkdocstrings, with doctests, type hints and Read the Docs builds."
sources:
  - https://peps.python.org/pep-0257/
  - https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
  - https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
  - https://mkdocstrings.github.io/python/
  - https://docs.readthedocs.com/platform/stable/config-file/v2.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Docstrings and API docs with Sphinx or mkdocstrings

**Goal:** public APIs documented once, in the code, rendered to a browsable site that fails the build when it rots.

## 1. Docstrings (PEP 257 + Google style)
```python
def fetch_rates(base: str, *, timeout: float = 5.0) -> dict[str, Decimal]:
    """Fetch current exchange rates relative to a base currency.

    Args:
        base: ISO 4217 code, e.g. ``"EUR"``.
        timeout: Seconds before the HTTP request is abandoned.

    Returns:
        Mapping of currency code to rate.

    Raises:
        RatesUnavailable: If the provider returns a non-200 response.

    Example:
        >>> fetch_rates("EUR")["USD"]  # doctest: +SKIP
        Decimal('1.0842')
    """
```
- First line: imperative summary that fits on one line; blank line; details.
- Document behaviour, units, side effects and exceptions; types live in the annotations (don't repeat them in prose).
- Every public module, class and function; private helpers only when non-obvious.

## 2. Sphinx
```python
# docs/conf.py
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon", "sphinx.ext.intersphinx",
              "sphinx.ext.viewcode", "sphinx_autodoc_typehints"]
autodoc_default_options = {"members": True, "undoc-members": False, "show-inheritance": True}
intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}
nitpicky = True
html_theme = "furo"
```
```rst
.. automodule:: mypkg.rates
   :members:
```
(Checked with Sphinx 9.2 and furo, sphinx-autodoc-typehints 3.17, mkdocs 1.6 with mkdocstrings-python 2.0: the config above builds, a misspelled `:class:` reference fails `sphinx-build -W` under `nitpicky`, and `mkdocs build --strict` fails on an unresolvable `[text][]` reference or a `:::` module that cannot be imported; an unresolved `[text][id]` inside a docstring did not fail it.) `sphinx-build -W --keep-going -b html docs docs/_build/html` turns warnings (broken refs, bad docstrings) into failures. `sphinx-apidoc -o docs/api src/mypkg` scaffolds pages; `autosummary` with `:recursive:` generates them at build time.

## 3. mkdocstrings (MkDocs)
```yaml
# mkdocs.yml
theme: { name: material }
plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          options: { docstring_style: google, show_source: false, merge_init_into_class: true }
```
In a Markdown page: `::: mypkg.rates`. `mkdocs build --strict` fails on warnings.

## 4. Doctests
`python -m pytest --doctest-modules src/` or `sphinx.ext.doctest`. Keep examples deterministic; mark network examples `+SKIP`.

## 5. Hosting
Read the Docs `.readthedocs.yaml` (version 2): build OS, Python version, `pip install .[docs]`, and `sphinx: { configuration: docs/conf.py, fail_on_warning: true }` (or `mkdocs.fail_on_warning`). Or build in CI and publish to GitHub Pages.

## Gotchas
- autodoc imports your modules: import-time side effects or heavy dependencies break the docs build; use `autodoc_mock_imports`.
- Mixed docstring styles confuse napoleon; pick one and enforce with ruff's `D` (pydocstyle) rules and `convention = "google"`.
- Docs that duplicate the README drift; link instead.

## Verify
- Docs build in CI with warnings as errors; deliberately misspell a cross-reference and confirm the build fails.
