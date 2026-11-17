---
id: computing-software.qa-testing-engineering.test-automation.data-driven-framework-design
name: data-driven-framework-design
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [data-driven-framework, data-driven-testing, parameterized-tests, test-data]
level: practitioner
status: docs-checked
description: "Design a data-driven test framework: separate test logic from data tables, parameterise in pytest and Playwright, validate data and keep rows independent."
sources:
  - https://docs.pytest.org/en/stable/how-to/parametrize.html
  - https://playwright.dev/docs/test-parameterize
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data-driven framework design

**Goal:** one test script runs against many data rows (inputs and expected results), so new cases are added as data, not code.

## Structure
- **Test logic:** a single parameterised test per behaviour.
- **Data source:** CSV or similar files in the repo (reviewable diffs), or generated data.
- **Loader:** reads, validates and turns rows into test parameters.

## pytest
`@pytest.mark.parametrize` takes argument names and a list of argument sets; the test runs once per set. Individual sets can carry marks via `pytest.param(..., marks=pytest.mark.xfail)`. Stacked decorators give all combinations. `pytest_generate_tests` with `metafunc.parametrize()` supports custom or dynamic schemes; an empty list skips the test. Parameter values are passed as-is (no copy), so tests must not mutate them.

```python
import csv, pathlib, pytest
ROWS = [(r['zone'], float(r['weight']), float(r['expected']))
        for r in csv.DictReader(pathlib.Path(__file__).with_name('shipping.csv').open())]

@pytest.mark.parametrize('zone,weight,expected', ROWS)
def test_shipping_cost(zone, weight, expected, api):
    assert api.quote(weight=weight, zone=zone).cost == pytest.approx(expected)
```

## Playwright
Loop over the data and create one `test()` per record with a unique title (the docs use `forEach` over an array, and a `for` loop over CSV records parsed with `csv-parse`). Put `beforeEach`/`afterEach` hooks outside the loop so they run once, or inside `test.describe()` to run per iteration. For configuration-level variation, Playwright "parameterized projects" run the same tests with different option values per project.

## Design rules
- Each row has a case id or description that goes into the test title, so a failure names the case.
- Expected results in the data come from the spec or an oracle, not from current system output.
- Validate the data file in a test (required columns, types) so a typo fails loudly, and assert it is non-empty, because an empty parameter list skips the test in pytest.
- Keep rows independent; shared setup belongs in fixtures or hooks.
- Do not hide control flow in data: a column that switches behaviour makes it a different design.

## Verify
Adding a new data row creates a new named test without code changes, and malformed data fails the validation test.

## Checked
2026-11-09: checked against the pytest "How to parametrize" and Playwright "Parameterize tests" pages, both read in full. The ISTQB CTAL-TAE overview page was read but it lists only syllabus headings and does not describe scripting approaches, so it was removed as a source along with the CTAL-TAE attribution in the goal line. The JUnit source was removed: the cited anchor returned only the JUnit overview page, so the `@CsvFileSource`/`@MethodSource` claims were dropped. Also removed: `ids=` usage, YAML/JSON, and the pairwise-tool advice, which none of the pages state. The tag `istqb-tae` was trimmed as unsupported.

Method: documentation only; no commands were run.
