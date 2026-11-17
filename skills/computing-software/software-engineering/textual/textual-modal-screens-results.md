---
id: computing-software.software-engineering.textual.textual-modal-screens-results
name: textual-modal-screens-results
category: computing-software
field: software-engineering
product: textual
tags: [textual, modal, modal-screen, screen-result, dismiss, push-screen-wait, callback]
level: practitioner
status: docs-checked
description: "Build Textual modal dialogs with ModalScreen, return data with dismiss and a push_screen callback, or await it with push_screen_wait inside a worker."
sources: [https://textual.textualize.io/guide/screens/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual modal screens and screen results

Goal: show a dialog over the current screen and get a typed result back.

## Method

1. Base the dialog on `ModalScreen` (from `textual.screen`) rather than `Screen`. It blocks App key bindings from being processed and sets a background with a little alpha so the previous screen shows through, darkened.
2. Return data by calling `dismiss(value)` on the screen. This pops it and calls the callback given to `push_screen`.

```python
class QuitScreen(ModalScreen[bool]):
    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Are you sure you want to quit?", id="question"),
            Button("Quit", variant="error", id="quit"),
            Button("Cancel", variant="primary", id="cancel"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit":
            self.dismiss(True)
        else:
            self.dismiss(False)
```

```python
    def action_request_quit(self) -> None:
        def check_quit(quit: bool | None) -> None:
            if quit:
                self.exit()

        self.push_screen(QuitScreen(), check_quit)
```

3. `ModalScreen[bool]` is optional typing: it tells the type checker that `dismiss` takes a bool and the callback receives the same type.
4. Waiting instead of a callback: `await self.push_screen_wait(screen)` returns the value passed to `dismiss`. It can only be used from a worker so the app keeps updating. Decorate the method with `@work` (for example the App mount handler) and call it inside.

Moving the exit decision into the caller's callback keeps the screen reusable and lets the app clean up before exiting.

## Gotchas

- With a plain `Screen` pushed from an App binding, pressing the key again pushes another copy (bindings on App are always checked), so multiple presses need multiple Cancel clicks. `ModalScreen` fixes this and also looks modal.
- `push_screen_wait` outside a worker is not allowed.

## Checked
2026-11-07. Read in full: Screens guide (modal, returning data, typing screen results, waiting for screens). Confirmed: ModalScreen blocks app bindings and sets an alpha background, dismiss(value) pops and calls the push_screen callback, ModalScreen[bool] typing, push_screen_wait only from a worker with @work, the plain-Screen repeated-push flaw. Removed: the Verify section (it described example output rather than a check).
Method: documentation only; no commands were run.
