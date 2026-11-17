---
id: computing-software.software-engineering.textual.textual-snapshot-testing
name: textual-snapshot-testing
category: computing-software
field: software-engineering
product: textual
tags: [textual, snapshot, pytest, snap-compare, pytest-textual-snapshot, visual-regression, testing, svg]
level: practitioner
status: docs-checked
description: "Catch visual regressions in a Textual app with pytest-textual-snapshot: snap_compare, the first failing run, --snapshot-update, press, terminal_size and run_before."
sources: [https://textual.textualize.io/guide/testing/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Snapshot testing Textual apps

Goal: record an SVG screenshot of your app and fail tests when later output differs.

## Method

1. Install the official plugin: `pip install pytest-textual-snapshot`. It provides the `snap_compare` fixture.
2. Write a test giving the path to the app file, relative to the test:

```python
def test_calculator(snap_compare):
    assert snap_compare("path/to/calculator.py")
```

3. Run `pytest`. The first run always fails (no previous snapshot to compare with) and prints a link to an HTML snapshot report; the report says "No history for this test".
4. Check the screenshot looks right, then save it as ground truth: `pytest --snapshot-update`. Only run this after running `pytest` and confirming the output looks good, since it accepts every screenshot in the report.
5. Run `pytest` again: the test passes because the new screenshot matches the saved one.
6. When a change breaks the visuals, `pytest` produces a report showing the saved snapshot on the right and the current render on the left; use the "Show difference" toggle (top right) to overlay them and spot subtle differences.
7. Options on `snap_compare`:

```python
snap_compare("path/to/calculator.py", press=["1", "2", "3"])
snap_compare("path/to/calculator.py", terminal_size=(50, 100))
```

`press` simulates keys before capture; `terminal_size` is `(width, height)`.
8. `run_before` runs async setup code with a pilot before the capture:

```python
def test_calculator_hover_number(snap_compare):
    async def run_before(pilot) -> None:
        await pilot.hover("#number-5")

    assert snap_compare("path/to/calculator.py", run_before=run_before)
```

## Gotchas

- Terminals may need Ctrl or Command held while clicking the report link.
- Snapshot tests work in CI on all supported operating systems; the report is an HTML file you can export as a build artifact.

## Checked
2026-11-07. Read in full: Testing guide (snapshot testing sections included). Confirmed: pip install pytest-textual-snapshot, snap_compare, first run always fails with No history for this test, --snapshot-update warning, right/left report layout and Show difference toggle, press, terminal_size (width, height), run_before with a pilot, link and CI tips. Removed: the Verify section.
Method: documentation only; no commands were run.
