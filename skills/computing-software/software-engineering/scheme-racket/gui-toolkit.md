---
id: computing-software.software-engineering.scheme-racket.gui-toolkit
name: gui-toolkit
category: computing-software
field: software-engineering
product: scheme-racket
tags: [racket, gui-toolkit]
level: advanced
status: docs-checked
description: "Build GUIs with racket/gui: frame%, button%, message%, callbacks run in the eventspace handler thread, and queue-callback for work from other threads."
sources:
  - https://docs.racket-lang.org/gui/
  - https://docs.racket-lang.org/gui/windowing-overview.html
  - https://docs.racket-lang.org/gui/frame_.html
  - https://docs.racket-lang.org/gui/button_.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# racket/gui windows and events
**Goal:** simple desktop UI.
```racket
#lang racket/gui
(define frame (new frame% [label "Example"]))
(define msg (new message% [parent frame] [label "No events so far..."]))
(new button% [parent frame] [label "Click Me"]
     [callback (lambda (button event) (send msg set-label "Button click"))])
(send frame show #t)
```
- Libraries: `racket/gui/base` (package gui-lib) provides the manual's classes and procedures plus `racket/draw`; `#lang racket/gui` combines `racket`, `racket/gui/base` and `racket/draw`.
- `frame%` is the top-level window; `label` shows in the title bar and `width` / `height` (default `#f`) give an initial size in pixels when larger than the minimum. Children such as `button%` take a `parent`; the `callback` takes the button and a control event and runs when the user clicks.
- Events are dispatched in the eventspace's handler thread; while a handler runs, no further events dispatch for that eventspace. A frame, dialog or timer belongs to the `current-eventspace` when created.
- Windowing functions can be called from any thread, but the manual advises doing all GUI setup and manipulation in the handler thread. Use `queue-callback` to schedule work there from another thread (optional second argument sets high or low priority); when already in the handler thread, use `yield` to wait on non-GUI events.
- `dialog%` is modal: when a handler thread shows one, `show` implicitly calls `yield` while it is shown.
## Self-check
Clicking the button changes the message text to "Button click".

## Checked
2026-11-08. Confirmed against the GUI manual front page, Windowing overview (1.1 Creating Windows, event dispatch and eventspaces), frame% and button% class pages: library and language names, example program, constructor arguments, callback signature, handler thread rules, queue-callback and yield advice. Removed: the web-server source (unrelated), `text-field%` (not checked), "requires the full Racket distribution" and the claim that `show` starts the event loop (neither stated).
Method: documentation only; no commands were run.
