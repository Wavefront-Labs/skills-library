---
id: computing-software.web-development.htmx.htmx-request-indicators
name: htmx-request-indicators
category: computing-software
field: web-development
product: htmx
tags: [htmx, hx-indicator, hx-disabled-elt, htmx-request, spinner, loading]
level: practitioner
status: docs-checked
description: "Show loading state during htmx requests with the htmx-indicator and htmx-request classes, hx-indicator selectors and hx-disabled-elt."
sources:
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/docs.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-indicator.md
  - https://raw.githubusercontent.com/bigskysoftware/htmx/master/www/content/attributes/hx-disabled-elt.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: give users feedback while a request is in flight.

Mechanism: htmx adds class `htmx-request` to the requesting element (or the element(s) named by `hx-indicator`) for the request duration. Elements with class `htmx-indicator` start at `opacity: 0`; inside (or on) an `htmx-request` element they fade to 1.

```html
<button hx-get="/click">Click Me!
  <img class="htmx-indicator" src="/spinner.gif" alt="Loading..."></button>
```

Explicit indicator: `hx-indicator` takes a CSS selector (all matches get the class) or `closest <selector>`. It is inherited. `inherit` keeps parent values and adds more: `hx-indicator="inherit, #spinner"`. The class may be put on any ancestor of the visible indicator.

Default CSS htmx injects: `.htmx-indicator{opacity:0;visibility:hidden}` and `.htmx-request .htmx-indicator, .htmx-request.htmx-indicator{opacity:1;visibility:visible;transition:opacity 200ms ease-in}`. For your own effect use a different class, e.g. `display:none` / `display:inline`. To keep the class name but supply your own CSS, set `includeIndicatorStyles` to `false`: `<meta name="htmx-config" content='{"includeIndicatorStyles": false}'>`. Under a strict nonce CSP set `inlineStyleNonce`, or disable the styles and host a stylesheet.

Disable controls: `hx-disabled-elt` adds the `disabled` attribute during the request. Values: selector, `this`, `closest <sel>`, `find <sel>`, `next [<sel>]`, `previous [<sel>]`, or a comma-separated list (not including `this`); `inherit` works too.
```html
<button hx-post="/example" hx-disabled-elt="this">Post It!</button>
```

Related config: `indicatorClass`, `requestClass`.

## Checked

2026-11-07. Confirmed against the htmx hx-indicator and hx-disabled-elt references and the docs Request Indicators and config sections (class mechanics, default CSS, `closest`, `inherit`, `includeIndicatorStyles`, `inlineStyleNonce`, CSP note, every `hx-disabled-elt` value form, `indicatorClass` and `requestClass`). Removed the invented Verify step; nothing else needed changing.
Method: documentation only; no commands were run.
