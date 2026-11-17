---
id: computing-software.software-engineering.textual.textual-command-palette
name: textual-command-palette
category: computing-software
field: software-engineering
product: textual
tags: [textual, command-palette, providers, system-commands, fuzzy-search, commands, tui]
level: practitioner
status: docs-checked
description: "Extend or disable the Textual command palette with get_system_commands, custom command Provider classes (search, discover), screen COMMANDS and key changes."
sources: [https://textual.textualize.io/guide/command_palette/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual command palette

Goal: add app commands to the built-in palette, or turn it off.

## Method

- Users press ctrl+p, type to fuzzy-search (matches letters in order, not only at the start: "ch" or "th" finds "Change theme"), select with up and down, and run with enter.
- Simple commands: override `get_system_commands(self, screen: Screen)` on the App; Textual calls it with the screen active when the palette opened. Yield `SystemCommand(title, help, callback)`. `discover` (default `True`) shows the command even with empty input; `False` shows it only when typing.

```python
def get_system_commands(self, screen: Screen) -> Iterable[SystemCommand]:
    yield from super().get_system_commands(screen)
    yield SystemCommand("Bell", "Ring the bell", self.bell)
```

  Keep `yield from super()...` to retain default commands.
- Custom providers: subclass `command.Provider` (`from textual.command import Provider, Hit`) and put it in the App's `COMMANDS` class var (for example `COMMANDS = App.COMMANDS | {PythonFileCommands}` keeps the default provider).
  - Methods (all `async def`; only `search` is required): `startup` (palette opened; prepare data), `search(self, query)` (yield `Hit` objects), `discover` (yield `DiscoveryHit` objects shown when input is empty; takes no parameters; keep it quick), `shutdown` (palette closed; clean up what startup created).
  - In `search`, use `matcher = self.matcher(query)` then `score = matcher.match(text)`. Zero means no hit; above zero is confidence, 1 being an exact match. `matcher.highlight(text)` highlights matching letters. A `Hit` takes the score, the display text, a callback, and optional help.
- Screen commands: set a `COMMANDS` class var on a Screen; they only apply while that screen is active.
- Disable: `ENABLE_COMMAND_PALETTE = False` on the App.
- Change key: `COMMAND_PALETTE_BINDING = "ctrl+backslash"` (the binding before 0.77.0).

## Gotchas

- Errors in a provider do not exit the app; they are logged to the devtools console.
- Providers must be coroutine methods.

## Verify

With the Bell example, pressing ctrl+p lists "Bell" and selecting it rings the terminal bell.

## Checked

2026-11-07: every claim was read against the full text of these pages: guide/command_palette. Nothing needed removing.

Method: documentation only; no commands were run.
