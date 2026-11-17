---
id: computing-software.software-engineering.wails.frameless-window-drag
name: frameless-window-drag
category: computing-software
field: software-engineering
product: wails
tags: [wails, go, frameless, window, drag, css, options]
level: practitioner
status: docs-checked
description: "Make a frameless Wails window draggable with the --wails-draggable CSS property or custom CSSDragProperty and CSSDragValue options."
sources: [https://wails.io/docs/guides/frameless, https://wails.io/docs/guides/frontend]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: build a frameless Wails app and mark which regions drag the window.

## Enable
Set `Frameless: true` in `options.App` (see the Frameless field in application options).

## Mark drag handles
Any element with the CSS style `--wails-draggable:drag` acts as a drag handle, and the property applies to its children. Opt a nested element out with `--wails-draggable:no-drag`:

```html
<body style="--wails-draggable:drag">
  <div id="logo"></div>
  <div id="input" style="--wails-draggable:no-drag">
    <input id="name" type="text" />
    <button onclick="greet()">Greet</button>
  </div>
</body>
```

## When CSS variables are not possible
For dynamic styling, choose another property/value pair with `CSSDragProperty` and `CSSDragValue`:

```go
Frameless:       true,
CSSDragProperty: "widows",
CSSDragValue:    "1",
```

and mark regions with it: `<body style="widows: 1">`.

## Gotcha
If the application is allowed to go fullscreen, dragging is disabled.

Note: the Frontend guide's sample HTML (its script injection example) uses `data-wails-drag` and `data-wails-no-drag` attributes without explaining them; the Frameless guide documents the CSS approach, which is what this skill describes.

## Checked

Date: 2026-11-07

Confirmed against the Wails v2 documentation source (wailsapp/wails, website/versioned_docs/version-v2.17.0), each cited page read in full: "Frameless Applications" guide; "Frontend" guide.

Corrected or removed: Replaced a hedged note about the data-wails-drag attributes with what the Frontend guide actually shows, and added that guide to sources.

Method: documentation only; no commands were run.
