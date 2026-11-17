---
id: computing-software.software-engineering.textual.textual-custom-widgets
name: textual-custom-widgets
category: computing-software
field: software-engineering
product: textual
tags: [textual, widget, custom-widget, static, default-css, scoped-css, links, border-title]
level: practitioner
status: docs-checked
description: "Build a custom Textual widget by subclassing Widget or Static, bundle styles in DEFAULT_CSS, add clickable markup links, set border titles and use Rich renderables."
sources: [https://textual.textualize.io/guide/widgets/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom Textual widgets

Goal: create a reusable widget that renders content, carries its own CSS and responds to clicks.

## Method

1. A widget manages a rectangular region of the screen, can respond to events like an app, and runs in its own asyncio task. Extend `Widget` (base of all widgets) or a subclass.
2. A `render()` method returns what is shown in the content area. Strings may contain content markup such as `[b]World[/]` for bold.
3. Prefer extending `Static`: it caches the result of `render` and provides `update()`. You then have no `render()` method; call `update()` when content changes (for example from a mount handler and a click handler).
4. Bundle CSS with the widget using the `DEFAULT_CSS` class variable (good for distributing a widget; for an app, an external stylesheet is better for live editing). Builtin widgets do this.
5. `DEFAULT_CSS` is scoped: it affects only the widget and potentially its children. Set the class variable `SCOPED_CSS = False` to disable that.
6. `DEFAULT_CSS` has automatically lower specificity than the App `CSS` class variable or an external stylesheet, so the app's CSS wins.
7. Links in text run an action when clicked:

```
"Click [@click=app.bell]Me[/]"
```

`@click` introduces a click handler that runs the action (`app.bell` here). Clickable text is underlined.
8. Every widget has `border_title` and `border_subtitle` (top and bottom border text). They show only if the widget has a border, default to an empty string (disabled), and defaults can be set with the `BORDER_TITLE` and `BORDER_SUBTITLE` class variables. Titles are one line; long text is cropped with an ellipsis. Color and alignment come from styles.
9. For advanced visuals, `render()` may return any Rich renderable (for example a Rich `Table`) or one from third-party libraries.

## Gotchas

- Subclass `Static` rather than `Widget` when you only need to display and update content.
- Border titles are invisible without a border.

## Verify

Run the app with `[b]World[/]` in a widget's render: `World` appears in bold. With `[@click=app.bell]Me[/]` the text is underlined and clicking runs the action.

## Checked

2026-11-07: every claim was read against the full text of these pages: guide/widgets. Nothing needed removing.

Method: documentation only; no commands were run.
