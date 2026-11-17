---
id: computing-software.software-engineering.scheme-racket.drracket-stepper
name: drracket-stepper
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, drracket-stepper, racket-drracket]
level: practitioner
status: docs-checked
description: "Use DrRacket's Step button in HtDP teaching languages and the Debug button (Go, Step, Over, Out, breakpoints, stack pane) in other languages."
sources:
  - https://docs.racket-lang.org/stepper/index.html
  - https://docs.racket-lang.org/drracket/buttons.html
  - https://docs.racket-lang.org/drracket/debugger.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stepper and debugger
**Goal:** trace execution in DrRacket.
- Stepper: the Step button appears only for the How to Design Programs teaching languages Beginning Student through Intermediate Student with Lambda (the Stepper manual names Beginning Student and Intermediate Student). It opens a window with before and after panes; the green region is the redex (next reducible expression), the purple region is its replacement. Each step swaps an expression for an equivalent one, e.g. `(+ 1 2)` becomes `3`.
- The Stepper only steps the definitions window; you cannot enter extra expressions, and a window with only function definitions yields no reductions.
- Debug button: not shown for the HtDP teaching languages. It runs the definitions window like Run but starts paused before the first expression (green triangle). Buttons: Go (until completion, breakpoint or unhandled exception), Step (one step), Over (enabled only at the start of a non-tail expression), Out, Pause (while running), Stop (cannot be continued).
- Breakpoints: hover a parenthesis showing a pink circle, right-click (Control-click on Mac OS) and choose Pause at this point (red circle) or Continue to this point (one-time, yellow circle). Clicking Run after debugging hides breakpoints; Debug restores them, but they do not persist across DrRacket restarts.
- While paused, hover a bound variable to see its value, right-click to print it or `(set! <var> ...)`; the stack view pane lists frames and lexical variables. To debug several files, open them all and click Debug in the main program's window.
- For macro expansion use the Macro Stepper instead.
## Self-check
In Beginning Student, step `(+ (* 2 3) 4)` and see `(* 2 3)` reduce to `6`, then the sum to `10`.

## Checked
2026-11-08. Confirmed against the Stepper manual (What is the Stepper, How do I use it), DrRacket Buttons (1.1) and Graphical Debugging Interface (1.8): language availability, redex colours, button semantics, breakpoint menus and persistence tips, stack view pane, multi-file debugging. Removed: the claim that breakpoints are set by right-clicking any expression (only a parenthesis with a pink circle offers the menu).
Method: documentation only; no commands were run.
