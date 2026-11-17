---
id: computing-software.web-development.htmx.htmx-hx-on-inline-handlers
name: htmx-hx-on-inline-handlers
category: computing-software
field: web-development
product: htmx
tags: [htmx, hx-on, inline-scripts, events, scripting, kebab-case]
level: practitioner
status: docs-checked
description: "Write inline handlers for any DOM or htmx event with hx-on:event, the hx-on:: shorthand, kebab-case names, dash syntax for JSX, and the deprecated hx-on form."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-on.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/docs.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: co-locate small event handlers with the element (Locality of Behaviour) for events HTML's `on*` attributes do not cover, especially htmx events.

Syntax: `hx-on:<event-name>="script"`.
```html
<div hx-on:click="alert('Clicked!')">Click</div>
```

Case gotcha: HTML attributes are case insensitive and the DOM lowercases them, so `hx-on:htmx:beforeRequest` will not work. htmx fires every event in camelCase and kebab-case, so use `hx-on:htmx:before-request`.

Shorthand: `hx-on::event` means `hx-on:htmx:event`:
```html
<button hx-get="/info"
        hx-on::before-request="alert('Making a request!')"
        hx-on::after-request="alert('Done making a request!')">Get Info!</button>
```
Add one attribute per event.

Template-friendly dashes (for JSX etc.): replace colons with dashes: `hx-on-htmx-before-request="..."` or shorthand `hx-on--before-request="..."`.

Modify a request inline:
```html
<button hx-post="/example"
        hx-on:htmx:config-request="event.detail.parameters.example = 'Hello Scripting!'">Post Me!</button>
```

Symbols available: `this` (the element with the attribute) and `event`.

Deprecated form: `hx-on="htmx:beforeRequest: alert('...')"`, multiple handlers on new lines. If an element has `hx-on:*` attributes, its `hx-on` value is ignored (the two forms can still be mixed across the document).

Notes: `hx-on` is not inherited, but events bubble, so a parent's handler normally sees children's events. `hx-on:*` needs eval; `htmx.config.allowEval=false` disables it. For camel-case-only events or complex logic use Alpine.js or hyperscript. Not a replacement for full scripting.

## Checked

2026-11-07. Confirmed on attributes/hx-on.md (syntax, case gotcha, `hx-on::` shorthand, dash forms, `config-request` example, `this` and `event`, deprecated form and its precedence, not inherited) and docs.md (scripting section and `allowEval`).
Removed: the invented Verify step.
Method: documentation only; no commands were run.
