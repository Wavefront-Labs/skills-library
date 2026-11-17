---
id: computing-software.software-engineering.textual.textual-content-markup
name: textual-content-markup
category: computing-software
field: software-engineering
product: textual
tags: [textual, content-markup, markup, content, rich-renderables, widgets, escaping]
level: practitioner
status: docs-checked
description: "Write Textual content markup tags, colors, links and click actions, build Content objects, substitute variables safely, and show Rich renderables."
sources: [https://textual.textualize.io/guide/content/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual content and markup

Goal: format widget content safely with markup, Content objects or Rich renderables.

## Method

Content comes from `Static.update` or a widget's `render()` as a markup string, a `Content` object, or a Rich renderable. Try markup live with `python -m textual.markup`.

Tags: `[bold]Hello[/bold], World!`. Overlapping tags combine. `[/]` auto-closes the last opened tag.

Styles: `bold` (`b`), `dim` (`d`), `italic` (`i`), `underline` (`u`), `strike` (`s`), `reverse` (`r`). Combine in one tag (`[bold italic]`); invert with `[not bold]...[/not bold]`.

Colors use CSS color syntax: `[#ff0000]`, `[chartreuse]`, `[rgba(0, 255, 0, 0.5)]`, `[auto on sienna]` (auto picks white or black), `[red 50%]` for opacity, `[on #ff0000 20%]` for background. Theme variables work: `[$accent]`, `[$warning on $warning-muted]`.

Links and actions:

```
[link="https://example.com"]Visit[/link]
Play the [@click=app.bell]bell[/]
Play the [on $success 30% @click=app.bell]bell[/]
```

Close an action explicitly with `[/@click=]`.

Escaping: a backslash before the open bracket (`\[bold]`) shows literal text; the guide also mentions an `escape` function (import path not given). Some methods take `markup=False`:

```python
self.notify(repr(my_list), markup=False)
```

Content class (immutable; methods return new instances):

```python
Content("hello, World!")                 # no markup processing
Content.from_markup("hello, [bold]World[/bold]!")
content = Content("Hello, World!").stylize(7, 12, "bold")
```

A string returned from `render()` is roughly `Content.from_markup(...)`.

Variables: avoid f-strings that inject user text, since brackets in the value become tags. Use string.Template syntax instead:

```python
return Content.from_markup("hello [bold]$name[/bold]!", name=name)
```

Rich renderables (for example `Text` or `Syntax`) display in a widget too, but Content is preferred for simple text because it supports more Textual features.

## Gotchas

- Heavily transparent colors can be hard to read.
- Plain `Content(...)` shows brackets literally.

## Verify

Rendering `\[bold]This is not bold` shows the text `[bold]This is not bold` unstyled.

## Checked

2026-11-07: every claim was read against the full text of these pages: guide/content. Removed the unverified textual.markup.escape module path; the page names only an escape function.

Method: documentation only; no commands were run.
