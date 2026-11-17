---
id: computing-software.qa-testing-engineering.test-case-design.golden-master-approval-testing
name: golden-master-approval-testing
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [golden-master, approval-testing, characterization-tests, snapshot-testing, legacy-code-testing, test-oracles, legacy-code-tests]
level: practitioner
status: verified
description: "Use golden master (approval/characterization) testing to lock in current behaviour of legacy code or complex outputs before refactoring, with scrubbers and review workflow."
sources:
  - https://approvaltests.com/
  - https://michaelfeathers.silvrback.com/characterization-testing
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Golden master / approval testing

**Goal:** when expected output is too large or unknown, record the current output as the oracle and detect any change. Feathers' characterization tests; ApprovalTests library.

## Workflow
1. Generate a broad, deterministic set of inputs (combinations of parameters, real anonymised samples).
2. Run the current system, save outputs as **approved** files (`*.approved.txt`), commit them. With ApprovalTests Python 20.0.0 the first run creates an empty approved file and fails, with names like `test_x.test_invoice_rendering.received.txt`.
3. Each test run produces `*.received.txt`; differences fail the test and open a diff tool.
4. Reviewer inspects the diff: intended change -> approve (copy received to approved); unintended -> bug.

```python
# approvaltests (Python)
from approvaltests import verify, verify_all_combinations
def test_invoice_rendering():
    verify(render_invoice(sample_order()))

def test_price_matrix():
    verify_all_combinations(price, [["bronze", "gold"], [0, 49.99, 50, 100], ["UK", "DE"]])
```
Java/C#/JS have equivalent ApprovalTests ports; Jest/Vitest `toMatchSnapshot` and pytest `syrupy` are lightweight variants.

## Scrubbing
Replace non-deterministic content before comparison: timestamps, GUIDs, random ids, absolute paths, ordering of sets. (`verify(text, options=Options().with_scrubber(create_regex_scrubber(pattern, "<ts>")))` from `approvaltests.scrubbers`; run, a timestamp became `<ts>` in the received file.) The `verify_all_combinations` call above writes one `args: (...) => result` line per combination.

## Use cases
- Refactoring legacy code with no tests (lock behaviour first).
- Reports, generated documents, rendered HTML/PDF text, large JSON responses, CLI output.

## Gotchas
- Approving without reading the diff turns the suite into a rubber stamp. Keep outputs human-readable and small enough to review.
- The golden master encodes existing bugs too; that is intended for refactoring, but note known bugs.

## Verify
Changing a calculation constant fails the relevant approval tests with a readable diff.
