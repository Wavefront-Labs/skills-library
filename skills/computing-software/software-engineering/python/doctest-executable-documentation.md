---
id: computing-software.software-engineering.python.doctest-executable-documentation
name: doctest-executable-documentation
category: computing-software
field: software-engineering
product: python
tags: [python, doctest, executable-documentation, doctest-modules, ellipsis, documentation-testing]
level: practitioner
status: verified
description: "Keep docstring and README examples correct with doctest: writing examples, option flags (ELLIPSIS, NORMALIZE_WHITESPACE), running via pytest, and when doctests are the wrong tool."
sources: ["https://docs.python.org/3/library/doctest.html", "https://docs.pytest.org/en/stable/how-to/doctest.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# doctest: executable documentation

**Goal:** examples in docs that are guaranteed to run, so they never rot.

## Writing examples
```python
def slugify(text: str) -> str:
    """Make a URL slug.

    >>> slugify("Hello, World!")
    'hello-world'
    >>> slugify("  multiple   spaces ")
    'multiple-spaces'
    >>> slugify(None)
    Traceback (most recent call last):
        ...
    TypeError: expected str, got NoneType
    """
```
The expected output is the `repr` printed by the interactive interpreter, compared as text.
Traceback examples need only the first line and the final exception line.

## Running
```bash
python -m doctest -v mymodule.py
python -m doctest README.md                    # text files too
pytest --doctest-modules src/                  # collect docstrings of all modules
pytest --doctest-glob="*.md" docs/
```
```toml
[tool.pytest.ini_options]
addopts = "--doctest-modules"
doctest_optionflags = "NORMALIZE_WHITESPACE ELLIPSIS"
```

## Handling non-deterministic output
```python
>>> obj                                   # doctest: +ELLIPSIS
<Client object at 0x...>
>>> sorted(d.items())                     # sort dicts/sets before printing
[('a', 1), ('b', 2)]
>>> print(f"{elapsed():.0f}")            # doctest: +SKIP
```
Flags: `ELLIPSIS` (`...` matches anything), `NORMALIZE_WHITESPACE`, `IGNORE_EXCEPTION_DETAIL`,
`SKIP`, `NUMBER` (pytest only: floats compared to written precision).

## Fixtures and setup
- pytest provides a `doctest_namespace` fixture to inject names:
```python
# conftest.py
@pytest.fixture(autouse=True)
def add_np(doctest_namespace):
    import numpy; doctest_namespace["np"] = numpy
```
- `getfixture('tmp_path')` inside a doctest pulls a pytest fixture.

## When not to use doctest
Complex setup, I/O, mocking or many edge cases belong in regular tests. Doctests are for
showing usage; a docstring with 40 lines of examples is a test file in disguise.

## Gotchas
- Blank lines in expected output need `<BLANKLINE>`.
- Output depends on Python version (repr changes, dict ordering is insertion-ordered since 3.7).
- Doctests in modules with import side effects run those side effects on collection.

## Verify
- [ ] CI runs `--doctest-modules` (and README doctests if examples exist there).
- [ ] No doctest relies on memory addresses, timestamps or unordered set output without flags.
