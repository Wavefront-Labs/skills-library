---
id: computing-software.software-engineering.scheme-racket.drracket-repl
name: drracket-repl
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, drracket-repl]
level: intro
status: docs-checked
description: "Use DrRacket's definitions window and interactions window: Run resets the REPL, pick the language via #lang or Choose Language, ESC-p recalls history."
sources:
  - https://docs.racket-lang.org/drracket/interactions-window.html
  - https://docs.racket-lang.org/drracket/choose-language.html
  - https://docs.racket-lang.org/drracket/buttons.html
  - https://docs.racket-lang.org/drracket/Menus.html
  - https://docs.racket-lang.org/drracket/Keyboard_Shortcuts.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Definitions window and REPL
**Goal:** use the IDE loop.
- The Run button evaluates the definitions window, makes its definitions available in the interactions window, and resets the interactions window: old interactions are erased and old definitions removed. F5 is the Run key.
- Language: either use the language declared in the source (Language > Choose Language... with "Use the language declared in the source", then start the program with `#lang`; this is the recommended mode) or pick a specific language in that dialog and click Run to apply it. A Custom indicator appears when the details differ from the default.
- Interactions window: type an expression after the `>` prompt and hit Enter; an incomplete expression gets an auto-indented new line instead, and Alt-Return (Command-Return on Mac) forces evaluation. Text before the last prompt cannot be edited. `ESC-p` / `ESC-n` cycle through old expressions, even after Run.
- Tab reindents the selection (the Reindent menu item); Reindent All indents the whole definitions or interactions window.
- Keys: `c:c;c:z` moves the cursor to the interactions window, `c:F6` moves between windows. With menu keybindings enabled (the Windows default), `c:e` toggles the visibility of the interactions window rather than moving to end of line. Use Edit > Show Active Keybindings for the authoritative list.
- The Break button interrupts an evaluation (click twice to kill it).
## Self-check
Define a function in the REPL only, press Run, and observe it vanishes.

## Checked
2026-11-08. Confirmed against the DrRacket manual pages Interactions Window (1.6), Choosing a Language (1.2), Buttons (1.1), Menus (Language and Edit) and Keyboard Shortcuts: Run semantics, language selection modes, Enter/Alt-Return behaviour, ESC-p/ESC-n, Tab as Reindent, c:e menu-binding note, c:c;c:z and c:F6, F5. Removed: "Ctrl+E toggles REPL focus" (the manual says it toggles interactions window visibility) and "Ctrl+I indents selection" (not found).
Method: documentation only; no commands were run.
