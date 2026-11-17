---
id: computing-software.qa-testing-engineering.jest-pytest.pytest-doctests
name: pytest-doctests
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [doctest, doctest-modules, documentation-testing, doctest-optionflags]
level: practitioner
status: verified
description: "Run doctests with pytest (--doctest-modules, --doctest-glob), configure optionflags like ELLIPSIS and NORMALIZE_WHITESPACE, use fixtures via getfixture and keep examples honest."
sources:
  - https://docs.pytest.org/en/stable/how-to/doctest.html
  - https://docs.python.org/3/library/doctest.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Doctests with pytest

## Enable
```toml
[tool.pytest.ini_options]
addopts = "--doctest-modules --doctest-glob='*.md'"
doctest_optionflags = ["NORMALIZE_WHITESPACE", "ELLIPSIS", "NUMBER"]
```
- `--doctest-modules` collects `>>>` examples from docstrings of every importable module under the paths.
- `--doctest-glob` adds text files (README.md, docs/*.rst).

## Example
```python
def slugify(s: str) -> str:
    """
    >>> slugify("Hello, World!")
    'hello-world'
    >>> slugify("  ")
    ''
    >>> sorted({"b", "a"})
    ['a', 'b']
    """
```

## Flags
- `ELLIPSIS`: `...` matches any text (`<object at 0x...>`).
- `NORMALIZE_WHITESPACE`: whitespace differences ignored.
- `NUMBER` (pytest): floats compare to the precision written (`3.14` matches `3.14159`).
- `IGNORE_EXCEPTION_DETAIL`: match exception type only.
Per example: `>>> x  # doctest: +SKIP`.

## Fixtures and namespace
```python
# conftest.py
@pytest.fixture(autouse=True)
def add_np(doctest_namespace):
    import numpy
    doctest_namespace["np"] = numpy
```
Inside a doctest: `>>> tmp = getfixture('tmp_path')`.

## When to use doctests
Short, deterministic usage examples in public APIs and README snippets, so documentation never shows broken code. Not for edge cases or complex setup: use regular tests.

## Gotchas
- Modules with import-time side effects (connecting to DBs) break `--doctest-modules`; exclude with `--ignore` or guard side effects.
- Dict/set ordering and object reprs make outputs unstable: sort, or use ELLIPSIS.
- Doctests in `if __name__ == "__main__"` blocks are not collected.

## Verify
Edit an example's expected output: `pytest --doctest-modules` fails with a "Expected/Got" diff.
