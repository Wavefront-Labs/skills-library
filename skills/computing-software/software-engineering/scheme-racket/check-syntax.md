---
id: computing-software.software-engineering.scheme-racket.check-syntax
name: check-syntax
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, check-syntax]
level: practitioner
status: docs-checked
description: "Inspect binding arrows, rename identifiers and jump between bindings and uses using DrRacket Check Syntax."
sources:
  - https://docs.racket-lang.org/drracket/buttons.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Check Syntax and Racket tooling
**Goal:** navigate code.
- Click the Check Syntax button to annotate the definitions window. Lexical structure is shown as arrows: pass the mouse over a variable and DrRacket draws an arrow from its binding location to the variable, or to every bound occurrence.
- Blue arrows are definite references. Purple arrows with a question mark are potential references inside macro definitions, because DrRacket cannot predict how the identifier will be used.
- Right-click (Control-click on Mac OS) a variable for a pop-up menu: jump from binding to bound location and vice versa, alpha-rename the variable, or tack the arrows so they stay.
- Documented identifiers are hyperlinked to their documentation page via right-click; right-clicking the argument of `require` lets you open the required module's file.
- Tail-position sub-expressions get a light purple arrow to the surrounding expression.
- Check Syntax also runs automatically as you edit. A red dot at the bottom right of the window means something went wrong; hover over it to see what.
## Self-check
Alpha-rename a function through the right-click menu and see the binding and its uses change together.

## Checked
2026-11-08. Read in full: DrRacket manual 1.1 Buttons (drracket/buttons.html), including the whole Check Syntax annotation list. The old source was only the manual root. Removed the unsupported claim that unbound identifiers show red (the page only says an unused require is coloured like an unbound variable) and the claim about racket-langserver/racket-mode editors (not on the page). Added the confirmed blue/purple arrow, require, tail-call and status-dot details.
Method: documentation only; no commands were run.
