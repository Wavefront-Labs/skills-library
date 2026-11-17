---
id: computing-software.software-engineering.textual.textual-testing-pilot
name: textual-testing-pilot
category: computing-software
field: software-engineering
product: textual
tags: [textual, testing, pilot, run-test, pytest, pytest-asyncio, headless, click]
level: practitioner
status: docs-checked
description: "Test a Textual app headlessly with run_test and the Pilot object: press keys, click widgets, set the screen size and pause for pending messages."
sources: [https://textual.textualize.io/guide/testing/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing Textual apps with the Pilot

Goal: automate user interaction in tests and assert on app state.

## Method

1. Textual is asyncio based, so use a test framework with asyncio support. The guide uses pytest with pytest-asyncio. That plugin needs `@pytest.mark.asyncio` on each async test unless you set `asyncio_mode = auto` in the pytest config or run `pytest --asyncio-mode=auto`.
2. Replace `app.run()` with `app.run_test()`: it runs the app headless (the terminal is not updated) and is an async context manager that yields a `Pilot`. Tests must be `async`.

```python
async def test_keys():
    app = MyApp()
    async with app.run_test() as pilot:
        await pilot.press("r")
        assert ...  # check the state you expect
```

(The guide's app has three buttons that change the background colour on r, g, b keys or clicks, and asserts the colour changed.)
3. Keys: `await pilot.press("h", "e", "l", "l", "o")`. Each string is one keypress; names like `"enter"` and modifiers like `"ctrl+"` use the same identifiers as key events (explore them with `textual keys`).
4. Clicks: `Pilot.click` with a CSS selector clicks the matching widget; for example `await pilot.click("#red")`. If another widget is in front, the topmost one gets the click, as for a real user.
   - No selector: click relative to the screen, `await pilot.click()` (at 0, 0).
   - `offset=(10, 5)` adds to the coordinates; combined with a selector it is relative to the widget: `await pilot.click(Button, offset=(0, -1))`.
   - `times=2` or `times=3` for double or triple click.
   - Modifiers: `shift`, `meta`, `control`, for example `await pilot.click("#slider", control=True)`.
5. Screen size defaults to (80, 24); change with `app.run_test(size=(100, 50))`.
6. Pending messages: after posting a message, `await pilot.pause()` waits for all pending messages to be processed before you assert; `delay` adds a wait first.
7. Run `pytest test_rgb.py`; failures from `assert` statements are recorded as test failures.

## Gotchas

- Asserting right after posting a message can fail because the message has not been processed yet; call `pause()`.

## Checked
2026-11-07. Read in full: Testing guide. Confirmed: pytest-asyncio marker and asyncio_mode=auto / --asyncio-mode=auto, run_test as async context manager yielding Pilot and headless, press with key names and ctrl+, textual keys, click with selector, no selector, offset, times, modifiers shift/meta/control, default size (80, 24) and size=, pause() with delay. Removed: the Verify section.
Method: documentation only; no commands were run.
