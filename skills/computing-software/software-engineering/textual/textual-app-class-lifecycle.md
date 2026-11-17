---
id: computing-software.software-engineering.textual.textual-app-class-lifecycle
name: textual-app-class-lifecycle
category: computing-software
field: software-engineering
product: textual
tags: [textual, app, lifecycle, compose, mount, exit, suspend, title]
level: practitioner
status: docs-checked
description: "Textual App basics: run options, compose and mount, awaiting mount, exit with a value or return code, suspend, CSS_PATH, and title or sub_title."
sources: [https://textual.textualize.io/guide/app/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual App class and lifecycle

Goal: structure a Textual App correctly from start to exit.

## Method

- Subclass `App`; call `App.run()` inside `if __name__ == "__main__":`.
- `run(inline=True)` shows the app beneath the prompt instead of application mode (since 0.55.0; not supported on Windows).
- `App(ansi_color=True)` keeps terminal ANSI colors instead of Textual's own (since 0.80.0); the default is recommended for full-screen apps.
- Event handlers are methods named `on_` plus the event name (`on_mount`, `on_key`). Handlers may be `async def`; Textual awaits coroutines.
- Add widgets at startup by implementing `compose()` and yielding widgets. Add them later with `mount()`.
- Mounting finishes by the next message handler, not right after the call. To change a just-mounted widget in the same handler, make the handler async and `await self.mount(Welcome())` before `self.query_one(Button).label = "YES!"`. Without the await, a `NoMatches` exception is raised.
- Exit with `self.exit(value)`; `run()` returns that value (or `None`). Subclass `App[str]` to type it: the return type is then `str | None`.
- Return code: `self.exit(return_code=4, message="Critical error occurred")`. A normal exit gives 0, an unhandled exception gives 1; read it from `app.return_code` (`None` if unset). Textual does not exit the process, so call `sys.exit(app.return_code or 0)` after `app.run()`.
- Suspend to run another terminal program (for example an editor):
  ```python
  with self.suspend():
      ...  # runs while the app is suspended
  ```
  Unavailable under textual-web. On Unix, ctrl+z suspending is disabled by default; bind a key to `action_suspend_process` to enable it (ignored on Windows and Textual Web).
- Styles: `CSS_PATH = "question02.tcss"` (relative to the file defining the app; `.tcss` is the usual extension) or a `CSS` class variable holding a CSS string.
- Title: `title` defaults to the App class name, `sub_title` to empty. Override with `TITLE` and `SUB_TITLE` class variables, or assign `self.title` / `self.sub_title` at runtime; the Header widget shows them and no manual refresh is needed.

## Gotchas

- Keeping `run()` under the `__name__` guard lets `textual run` and imports work.
- Do not expect `mount()` results to be queryable until awaited or the next handler.

## Verify

The page's `QuestionApp(App[str])` with Yes and No buttons calling `self.exit(event.button.id)` makes `app.run()` return `"yes"` or `"no"` depending on the button clicked.

## Checked

2026-11-07: every claim was read against the full text of these pages: guide/app. Corrected the CSS_PATH filename to the one in the page's code (question02.tcss).

Method: documentation only; no commands were run.
