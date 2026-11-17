---
id: computing-software.software-engineering.textual.textual-screens-stack
name: textual-screens-stack
category: computing-software
field: software-engineering
product: textual
tags: [textual, screens, screen-stack, push-screen, pop-screen, switch-screen, install-screen, tui]
level: practitioner
status: docs-checked
description: "Create Textual Screen subclasses, name them with SCREENS or install_screen, and move between them with push_screen, pop_screen and switch_screen."
sources: [https://textual.textualize.io/guide/screens/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual screens and the screen stack

Goal: define screens and control which one is active.

## Method

- A screen is a container for widgets that fills the terminal; only one is active at a time. The App creates one implicit default screen, which receives widgets you mount or compose unless you change screens.
- Create one by extending `Screen` from `textual.screen`. It is styled like other widgets, except you cannot change its dimensions. It can have `BINDINGS` and `compose()` like an App.
- Name screens with a `SCREENS` dict on the App (name to screen), or call `install_screen` (for example in a mount handler). Names and screen objects are interchangeable in the screen API. Prefer `SCREENS` for screens that live for the whole app. Installed screens stay in memory until `uninstall_screen`.
- The stack: only the top screen renders and receives input.
  - `push_screen` puts a screen (name or object) on top and activates it.
  - `pop_screen` removes the top screen; the one below becomes active. It is deleted unless installed or present elsewhere on the stack.
  - `switch_screen` replaces the top of the stack; the replaced screen is removed and deleted unless installed.
- Actions: `app.push_screen` (needs the name of an installed screen), `app.pop_screen`, and `app.switch_screen` (takes a screen name). Example binding: `("b", "push_screen('bsod')", "BSOD")` on the App and `("escape", "app.pop_screen", "Pop screen")` on the Screen.
- A screen background with an alpha component (for example `rgba(0,0,255,0.5)`) blends with the screen beneath; only the top screen is active.
- Screen events: `ScreenSuspend` is sent to a screen that becomes inactive (another pushed, or a mode switch); `ScreenResume` is sent to the newly active screen. Use them to pause work on hidden screens.

## Gotchas

- The stack must keep at least one screen; popping the last raises `ScreenStackError`.
- Bindings defined on App are always checked, so an App-level key that calls `push_screen` pushes another copy every press (see textual-modal-screens-results for `ModalScreen`).

## Checked
2026-11-07. Read in full: Screens guide. Confirmed: Screen creation and styling limits, SCREENS vs install_screen/uninstall_screen, push/pop/switch semantics and their actions, ScreenStackError, background alpha, ScreenSuspend/ScreenResume. Corrected: the Screen escape binding action is app.pop_screen (not pop_screen). Removed: the Verify section.
Method: documentation only; no commands were run.
