---
id: computing-software.web-development.svelte.event-attributes-delegation
name: event-attributes-delegation
category: computing-software
field: web-development
product: svelte
tags: [event-attributes, onclick, event-delegation, svelte-events-on, passive-touch-events]
level: practitioner
status: docs-checked
description: "Svelte 5 DOM events as on-prefixed attributes: case sensitivity, ordering after bindings, passive touch handlers, and event delegation gotchas."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/03-template-syntax/01-basic-markup.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Listen with attributes starting with `on`: `<button onclick={() => console.log('clicked')}>`. Names are case sensitive (`onClick` listens to `Click`, so custom events with capitals work). Shorthand `{onclick}` and spreading work as for any attribute.

Timing: event attributes fire after events from bindings, so `oninput` runs after `bind:value` updated.

`ontouchstart` and `ontouchmove` handlers are passive. If you must call `preventDefault()` there, use `on` from `svelte/events` (for example inside an action).

Delegation: for some events a single listener at the application root runs handlers on the event path. Gotchas:
- A manually dispatched event needs `{ bubbles: true }` to reach the root.
- With raw `addEventListener`, `stopPropagation` stops the event reaching the root, so handlers are not invoked. Handlers added manually inside the root run before declarative ones, in both phases.
- Prefer `on` from `svelte/events`, which preserves order and handles `stopPropagation`.

Delegated events: `beforeinput`, `click`, `change`, `dblclick`, `contextmenu`, `focusin`, `focusout`, `input`, `keydown`, `keyup`, `mousedown`, `mousemove`, `mouseout`, `mouseover`, `mouseup`, `pointerdown`, `pointermove`, `pointerout`, `pointerover`, `pointerup`, `touchend`, `touchmove`, `touchstart`.

## Checked

Method: docs-only read of cited pages, 2026-11-08
