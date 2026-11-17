---
id: computing-software.software-engineering.textual.textual-app-modes
name: textual-app-modes
category: computing-software
field: software-engineering
product: textual
tags: [textual, modes, switch-mode, default-mode, screens, screen-stack, navigation]
level: practitioner
status: docs-checked
description: "Give a Textual app several independent screen stacks with the MODES dict, DEFAULT_MODE and switch_mode, such as dashboard, settings and help."
sources: [https://textual.textualize.io/guide/screens/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual modes (multiple screen stacks)

Goal: let users jump between top-level areas of an app while each keeps its own push/pop navigation.

## Method

A mode is a named screen stack. Switching mode makes the topmost screen of that mode's stack visible. Modes suit apps with independent areas (dashboard, settings, help) where a modal screen on one stack should not stop the user switching.

1. Define `MODES` on the App: a dict mapping a mode name to a screen object, a callable returning a screen, or the name of an installed screen. These values set the base screen of each stack.
2. Switch with `App.switch_mode("name")`, or bind keys to the built-in `switch_mode` action.
3. Optionally set `DEFAULT_MODE` to choose the mode active at startup.
4. `push_screen` and `pop_screen` affect only the active mode's stack.

```python
class ModesApp(App):
    BINDINGS = [
        ("d", "switch_mode('dashboard')", "Dashboard"),
        ("s", "switch_mode('settings')", "Settings"),
        ("h", "switch_mode('help')", "Help"),
    ]
    MODES = {
        "dashboard": DashboardScreen,
        "settings": SettingsScreen,
        "help": HelpScreen,
    }

    def on_mount(self) -> None:
        self.switch_mode("dashboard")
```

Here `DashboardScreen`, `SettingsScreen` and `HelpScreen` are `Screen` subclasses (each composes a `Placeholder` and a `Footer`). On startup the app switches to the dashboard mode; pressing d, s or h swaps modes.

Screens that become inactive through a mode switch receive `ScreenSuspend`, and the newly visible one receives `ScreenResume`.

## Gotchas

- Do not mix up modes with the single stack: pushing a screen in one mode does not appear in another mode.
- The page shows both `on_mount` with `switch_mode("dashboard")` and the `DEFAULT_MODE` class variable as ways to pick the starting mode.

## Verify

Run the example: the dashboard placeholder shows first; pressing s shows the settings screen and h the help screen, and d returns to the dashboard.

## Checked

2026-11-07: every claim was read against the full text of these pages: guide/screens. Nothing needed removing.

Method: documentation only; no commands were run.
