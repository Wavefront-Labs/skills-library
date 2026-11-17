---
id: computing-software.software-engineering.textual.textual-text-styling
name: textual-text-styling
category: computing-software
field: software-engineering
product: textual
tags: [textual, styles-reference, text-style, text-align, text-wrap, text-overflow, ellipsis, nowrap]
level: practitioner
status: docs-checked
description: "Style Textual text with text-style, text-align, text-wrap and text-overflow, including accepted values and the Python property names."
sources: [https://textual.textualize.io/styles/text_style/, https://textual.textualize.io/styles/text_align/, https://textual.textualize.io/styles/text_wrap/, https://textual.textualize.io/styles/text_overflow/, https://textual.textualize.io/css_types/text_style/, https://textual.textualize.io/css_types/text_align/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual text styling

Goal: control weight, alignment, wrapping and overflow of text inside a widget.

## Method

### text-style

`text-style: <text-style>;` is `none` or a space-separated combination of `bold`, `italic`, `reverse` (swap foreground/background), `strike`, `underline`.

```css
text-style: italic;
text-style: strike bold italic reverse;
```

```python
widget.styles.text_style = "italic"
```

### text-align

`text-align: <text-align>;` default `start`. Values: `left`, `center`, `right`, `justify`, plus `start` (alias for left) and `end` (alias for right); the meaning of start/end will likely change when right-to-left languages are supported.

```python
widget.styles.text_align = "right"
```

### text-wrap

`text-wrap: wrap | nowrap;` default `wrap` (word wrap). `nowrap` disables wrapping, giving a single line.

```python
widget.styles.text_wrap = "nowrap"
```

### text-overflow

`text-overflow: clip | fold | ellipsis;` applies when text does not fit a line, which happens if wrapping is disabled or one word is wider than the container.

- `clip`: overflowing part removed.
- `fold`: overflow continues on the next line(s), ignoring word boundaries so words may be split.
- `ellipsis`: truncated, last visible character replaced with an ellipsis; signals there may be more text.

```css
#widget {
    text-overflow: ellipsis;
}
```

```python
widget.styles.text_overflow = "ellipsis"
```

## Gotchas

- `text-align` aligns text inside the widget; `align` positions child widgets in a container and `content-align` positions content inside a widget.
- The `<text-style>` and `<text-align>` types are not the same thing as the rules of the same name.

## Checked
2026-11-07. Read in full: text-style, text-align, text-wrap and text-overflow style pages and the <text-style> and <text-align> type pages. Confirmed: allowed values, text-align default start and start/end aliases with the RTL caveat, text-wrap default wrap, text-overflow clip/fold/ellipsis semantics, Python property forms, see-also distinctions from align and content-align, type-versus-rule warning. Removed: the Verify section.
Method: documentation only; no commands were run.
