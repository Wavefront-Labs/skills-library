---
id: computing-software.software-engineering.javascript.js-event-propagation-capture
name: js-event-propagation-capture
category: computing-software
field: software-engineering
product: javascript
tags: [javascript, event-capture-phase, js-dom-events]
level: practitioner
status: docs-checked
description: "Understand capture, target and bubble phases, eventPhase, stopPropagation versus stopImmediatePropagation, and composedPath."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/Event/eventPhase", "https://developer.mozilla.org/en-US/docs/Web/API/Event/stopPropagation", "https://developer.mozilla.org/en-US/docs/Web/API/Event/stopImmediatePropagation", "https://developer.mozilla.org/en-US/docs/Web/API/Event/composedPath", "https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Event propagation and capture

- Phases: capturing starts at the Window, then Document, `html` and so on down to the target's parent; then the target phase; then bubbling back up to the Window, which happens only if `event.bubbles` is true. If `bubbles` is false, processing ends after the target phase.
- Listeners registered with the capture option fire during the capturing phase.
- `stopPropagation()` stops further propagation in the capture and bubble phases but does not stop other listeners on the current element; `stopImmediatePropagation()` stops those too. Neither prevents default behaviour; use `preventDefault()` for that.
- `event.eventPhase` reports the current phase as a number: 0 none, 1 capturing, 2 target, 3 bubbling.
- `event.composedPath()` returns the array of objects on which listeners will be invoked, excluding nodes inside closed shadow roots.
- Overusing `stopPropagation` can hide events from other listeners higher in the tree.

Self-check: log `event.eventPhase` in a capture listener on a parent and a normal listener on the clicked child.

## Checked

2026-11-03. Confirmed on MDN: Event.eventPhase (phase descriptions and the none/capturing/target/bubbling numbering from the example), Event.stopPropagation, Event.stopImmediatePropagation, Event.composedPath, EventTarget.addEventListener (capture option). Removed: which events do not bubble and the `focusin`/`focusout`/`mouseover` advice (not on a page read), and the claim about breaking analytics and delegation.
Method: documentation only; no commands were run.
