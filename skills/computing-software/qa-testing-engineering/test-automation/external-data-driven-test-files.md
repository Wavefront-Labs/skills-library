---
id: computing-software.qa-testing-engineering.test-automation.external-data-driven-test-files
name: external-data-driven-test-files
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [external-test-data, data-driven-testing, test-data-management, csv-test-data, parametrized-tests]
level: practitioner
status: docs-checked
description: "Drive tests from external CSV files: loaders for pytest and Playwright, case IDs in test titles, data-file validation and hygiene."
sources:
  - https://docs.pytest.org/en/stable/how-to/parametrize.html
  - https://playwright.dev/docs/test-parameterize
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# External data-driven test files (CSV)

**Goal:** separate test data from test logic so analysts can add cases without coding, while keeping failures traceable.

## pytest
`@pytest.mark.parametrize` defines multiple argument sets for a test function; the function runs once per set, and a failing set is reported with its values in the test id (for example `test_eval[6*9-42]`). Parameter values are passed as-is, not copied, so a test that mutates a list or dict parameter changes it for later cases. Do not mutate them.

```python
import csv, pathlib, pytest

def load(name):
    path = pathlib.Path(__file__).parent / "data" / name
    with open(path, newline="", encoding="utf-8") as f:
        return [(r["country"], int(r["weight_g"]), int(r["expected_fee"])) for r in csv.DictReader(f)]

@pytest.mark.parametrize("country,weight_g,expected_fee", load("shipping_cases.csv"))
def test_shipping(country, weight_g, expected_fee):
    assert shipping_fee(country, weight_g) == expected_fee
```

- `pytest.param(..., marks=pytest.mark.xfail)` marks an individual case, for example a known defect.
- For custom schemes, the `pytest_generate_tests` hook calls `metafunc.parametrize()` while a test is collected. If it is given an empty parameter list the test is skipped ("got empty parameter set"); a data file that loads as zero rows therefore silently skips the test rather than failing it, so assert the row count.
- Stacking two `parametrize` decorators runs all combinations.

## Playwright
The Playwright runner is Node.js, so it can read files and parse them with a CSV library. The documented pattern generates one test per record with the case name in the title:
```ts
import fs from 'fs';
import path from 'path';
import { test } from '@playwright/test';
import { parse } from 'csv-parse/sync';

const records = parse(fs.readFileSync(path.join(__dirname, 'input.csv')), {
  columns: true,
  skip_empty_lines: true
});

for (const record of records) {
  test(`foo: ${record.test_case}`, async ({ page }) => { /* ... */ });
}
```
Test names must be unique. Put `beforeEach`/`afterEach` hooks outside the loop so they run once, or inside a `test.describe()` per iteration if each case needs its own hook. Keep credentials out of data files; Playwright documents passing them as environment variables.

## Data file hygiene
- First column a stable case id (the example file uses `test_case`) and use it in the test title.
- Columns for inputs, expected results and a reason (requirement, boundary, defect id).
- Validate the file in CI (a test that loads every row and checks required columns and types) so a typo fails fast.
- Keep data files next to tests in the repo, reviewed in pull requests; no secrets.
- CSV is all strings; convert and validate types, including empty cells.

## Gotchas
- Spreadsheets saved as CSV can change encodings, delimiters and number formats; standardise on UTF-8 and `,`.
- Huge data files make failures hard to read; split by intent.

## Verify
Data files load through a validation test in CI, every row reports as its own test, and adding a row needs no code change.

## Checked
2026-11-09: checked against the pytest "How to parametrize" page (parametrize, pytest.param marks, as-is values, pytest_generate_tests and the empty-set skip, stacking) and Playwright "Parameterize tests" (forEach pattern, hooks placement, CSV with csv-parse, environment variables for secrets), both read in full. Removed: the JUnit `@CsvFileSource` section and its source (the cited JUnit anchor returned only the overview page, so the parameter-source claims could not be confirmed), `pytest.param(id=...)`, YAML/JSON loader advice and the Excel date auto-conversion claim, none stated by the pages.

Method: documentation only; no commands were run.
