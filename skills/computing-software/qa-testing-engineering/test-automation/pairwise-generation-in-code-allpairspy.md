---
id: computing-software.qa-testing-engineering.test-automation.pairwise-generation-in-code-allpairspy
name: pairwise-generation-in-code-allpairspy
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [pairwise-in-code, allpairspy, pairwise-testing, combinatorial-testing, pytest-parametrize]
level: practitioner
status: verified
description: "Generate pairwise combinations in test code with allpairspy and feed them to pytest parametrize, with filters for invalid combinations and stable IDs."
sources:
  - https://github.com/thombashi/allpairspy
  - https://docs.pytest.org/en/stable/how-to/parametrize.html
  - https://www.pairwise.org/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pairwise generation in code (allpairspy)

**Goal:** keep combinatorial cases next to the test, regenerated automatically when parameters change.

## Basic use
```python
from collections import OrderedDict
import pytest
from allpairspy import AllPairs

PARAMS = OrderedDict({
    "browser": ["chrome", "firefox", "webkit"],
    "locale": ["en-GB", "de-DE", "ja-JP"],
    "payment": ["card", "paypal"],
    "guest": [True, False],
})

def valid(row):
    # row is a partial list while generating; check only fields present
    if len(row) > 2 and row[0] == "webkit" and row[2] == "paypal":
        return False            # unsupported combination
    return True

CASES = list(AllPairs(PARAMS, filter_func=valid))   # namedtuples when given an OrderedDict

@pytest.mark.parametrize("case", CASES, ids=lambda c: "-".join(map(str, c)))
def test_checkout(case, page):
    run_checkout(page, **case._asdict())
```
3 x 3 x 2 x 2 = 36 full combinations; pairwise needs about 9-10. Run on allpairspy 2.5.1 with pytest 9: the block generated 9 cases (also 9 without the filter), rows are `Pairs` namedtuples (`case._asdict()` works), a coverage script found every pair present except `webkit`+`paypal`, which the filter removes on purpose (so that pair is never covered, by design), and the filter was called with rows of length 1 to 4.

## Filter rules
`filter_func` receives the row built so far (length grows as parameters are added); return False to reject. Write it to handle partial rows, or invalid pairs slip through.

## Alternatives
- Java: JUnit 5 with a generated CSV (PICT/ACTS) via `@CsvFileSource`, or the `junit-pioneer`/third-party pairwise extensions.
- JS: generate a CSV with PICT in a pre-step and load it in `test.each`.
- Hypothesis is random, not pairwise; complementary.

## Stability
- Generation order follows parameter and value order; changing either reshuffles cases, so IDs change. Use descriptive IDs (values joined), not indexes.
- Pin the library version; algorithm changes alter the set.
- For audit needs, write the generated set to a file and commit it.

## Gotchas
- allpairspy covers pairs only (no higher strength); use PICT `/o:3` or ACTS for t >= 3.
- Large suites at collection time slow pytest startup; cache the list at module import, as above.

## Verify
Count of generated cases is far below the full product, a pair-check script confirms every valid value pair appears, and no filtered combination appears.
