---
id: computing-software.software-engineering.python.subtests-and-parametrised-cases
name: subtests-and-parametrised-cases
category: computing-software
field: software-engineering
product: python
tags: [python, py-unit-testing, subtest-parametrize, subtest, pytest-parametrize, table-driven-tests, ids, unittest]
level: practitioner
status: draft
description: "Write table-driven tests with unittest subTest and pytest.mark.parametrize: readable ids, pytest.param marks, stacked parametrisation and when to use each."
sources: ["https://docs.python.org/3/library/unittest.html#distinguishing-test-iterations-using-subtests", "https://docs.pytest.org/en/stable/how-to/parametrize.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Subtests and parametrised cases

## unittest.subTest
```python
import unittest

class TestSlug(unittest.TestCase):
    def test_cases(self):
        cases = [("Hello World", "hello-world"), ("  a  b ", "a-b"), ("Ünï", "uni")]
        for raw, expected in cases:
            with self.subTest(raw=raw):            # a failure is reported, loop CONTINUES
                self.assertEqual(slugify(raw), expected)
```
One test method, many reported results; failures print the subTest parameters. Good for stdlib-only suites.

## pytest.mark.parametrize
```python
import pytest

@pytest.mark.parametrize(
    "raw, expected",
    [
        pytest.param("Hello World", "hello-world", id="spaces"),
        pytest.param("  a  b ", "a-b", id="collapse"),
        pytest.param("", "", id="empty"),
        pytest.param("x" * 300, "x" * 300, id="long", marks=pytest.mark.slow),
        pytest.param("Ünï", "uni", marks=pytest.mark.xfail(reason="issue 42", strict=True)),
    ],
)
def test_slugify(raw, expected):
    assert slugify(raw) == expected

@pytest.mark.parametrize("x", [0, 1])
@pytest.mark.parametrize("y", [10, 20])     # stacked decorators = cartesian product (4 tests)
def test_grid(x, y): ...
```
Select a single case: `pytest "tests/test_slug.py::test_slugify[empty]"`; list ids with `--collect-only -q`.

## Choosing
| Situation | Use |
|---|---|
| each case should be an independent test (own fixtures, marks, selectable, xdist-parallel) | `parametrize` |
| cases share expensive setup, or the case list is computed inside the test | `subTest` (pytest supports it via the `pytest-subtests` plugin; core support is in progress) |
| generated data | `parametrize(argvalues=load_cases())` or Hypothesis |

## Gotchas
- Always give ids to non-trivial objects; default ids like `obj0` are useless. `ids=callable` or `pytest.param(id=...)`.
- Parametrize evaluates the list at collection time: no network or DB calls there.
- Mutable parameters shared across cases; build them inside the test or use fixtures.
- `subTest` failures inside `setUp`-heavy classes still share state between iterations.
- Parameter names must be function arguments; with indirect fixtures use `indirect=True`.

## Verify
- [ ] Intentionally break one case: the report names it (id or subTest params) and others still run.
- [ ] `pytest --collect-only -q | head` shows readable ids.
