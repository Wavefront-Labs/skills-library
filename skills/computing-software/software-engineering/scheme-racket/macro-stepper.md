---
id: computing-software.software-engineering.scheme-racket.macro-stepper
name: macro-stepper
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, macro-stepper, racket-macro-debug]
level: practitioner
status: docs-checked
description: "Step through macro expansion with macro-debugger: expand/step, expand-module/step, macro-stepper-repl, expand/step-text and the syntax browser."
sources:
  - https://docs.racket-lang.org/macro-debugger/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Macro Stepper
**Goal:** see each expansion step.
```racket
(require macro-debugger/stepper)
(expand/step #'(let ([x 1] [y 2]) (or (even? x) (even? y))))
(expand-module/step "my-module.rkt")   ; file must hold a single module declaration
```
- `macro-debugger/stepper` (package macro-debugger) opens a stepper frame: `expand/step` takes syntax or an S-expression, `expand-module/step` takes a module path, and `macro-stepper-repl` shows the expansion of every expression entered at a REPL (`#:eval?` defaults to `#t`).
- Text only: `(require macro-debugger/stepper-text)` (package macro-debugger-text-lib) gives `expand/step-text stx [show?]`, which prints each step; `show?` is an identifier predicate or a list of identifiers to show. In XREPL, `,syntax` with the `*` or `**` flag uses it.
- Navigation: step forward or backward, jump to the start or end; "Previous term" / "Next term" move between expansions when several are shown.
- Macro hiding: in the bottom panel select an identifier in the syntax browser and click "Hide module", "Hide macro" or "Show macro". Hidden macros are treated as primitive but their subterms are still expanded. Hiding also skips steps such as internal defines becoming `letrec`.
- Syntax browser colours: terms with the same foreground colour have the same marks, i.e. they were in the original syntax or came from the same macro step; black means unmarked syntax (original, or from a non-hygienic macro).
- Macros can send notes to a listening stepper with `emit-remark` from `macro-debugger/emit`.
- `macro-debugger/expand` provides `expand-only` and `expand/hide`, but hiding is selective, so the result may not evaluate the same as the original syntax.
## Self-check
Step the `or` example above and watch it expand to a `let` binding `or-part` and an `if`.

## Checked
2026-11-08. Confirmed against the Macro Debugger manual (sections 1-7): module names and packages, procedure names and arguments, text interface, navigation, macro hiding policy, colour partition meaning, emit-remark, the hiding warning, and the `or` expansion example. Removed: the DrRacket toolbar-button instruction and the `racket -l macro-debugger/...` entry point (neither appears on the page).
Method: documentation only; no commands were run.
