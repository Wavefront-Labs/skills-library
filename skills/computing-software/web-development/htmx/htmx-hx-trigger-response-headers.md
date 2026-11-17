---
id: computing-software.web-development.htmx.htmx-hx-trigger-response-headers
name: htmx-hx-trigger-response-headers
category: computing-software
field: web-development
product: htmx
tags: [htmx, hx-trigger, response-headers, client-events, hx-trigger-after-swap, from-body]
level: practitioner
status: docs-checked
description: "Fire client events from the server with HX-Trigger, HX-Trigger-After-Swap and HX-Trigger-After-Settle: JSON details, target, multiple events."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/headers/hx-trigger.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-trigger.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let a server response cause client-side events (toasts, refreshes of other widgets).

Three headers, differing in timing:
- `HX-Trigger` - as soon as the response is received.
- `HX-Trigger-After-Swap` - after the swap step.
- `HX-Trigger-After-Settle` - after the settle step.

Forms of the value:
- Plain name: `HX-Trigger: myEvent` - fires on the triggering element and bubbles to `body`.
- JSON with detail: `HX-Trigger: {"showMessage":"Here Is A Message"}` - the string lands in `evt.detail.value`.
- JSON with an object: `HX-Trigger: {"showMessage":{"level":"info","message":"Hi"}}` - each property is copied onto `evt.detail` (`evt.detail.level`, `evt.detail.message`).
- Another element: add `target`: `HX-Trigger: {"showMessage":{"target":"#otherElement"}}`.
- Several events: `HX-Trigger: {"event1":"A message","event2":"Another message"}` or, without details, `HX-Trigger: event1, event2`.

Listening:
```javascript
document.body.addEventListener("showMessage", e => alert(e.detail.value));
```
Or declaratively, remembering the event bubbles from a different DOM branch, so use `from:body`:
```html
<div hx-trigger="myEvent from:body" hx-get="/example"></div>
```

Gotcha: response headers are not processed on 3xx responses (the browser follows the redirect internally); return 200 instead.

## Checked

2026-11-07. Confirmed on headers/hx-trigger.md (three headers and timing, plain and JSON forms, `detail.value`, `target`, multiple events, 3xx note) and attributes/hx-trigger.md (`from:body`).
Removed: the invented Verify step.
Method: documentation only; no commands were run.
