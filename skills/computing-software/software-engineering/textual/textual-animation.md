---
id: computing-software.software-engineering.textual.textual-animation
name: textual-animation
category: computing-software
field: software-engineering
product: textual
tags: [textual, animation, animate, easing, duration, opacity, offset, on-complete]
level: practitioner
status: docs-checked
description: "Animate Textual styles such as opacity and offset with animate, choosing duration or speed, easing functions, delay and completion callbacks."
sources: [https://textual.textualize.io/guide/animation/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual animation

Goal: change a style or attribute smoothly over time.

## Method

- The animator moves a value to a target in small increments. Apps and widgets have an `animate` method for their own properties, and `styles` objects have an identical `animate` for styles such as `offset` (movement) and `opacity` (fading).
- Fade a widget out over two seconds:

```python
def on_mount(self):
    self.box.styles.animate("opacity", value=0.0, duration=2.0)
```

- Choose `duration` (seconds the animation takes) or `speed` (units the value changes per second). Animating from 0 to 10 with speed 2 completes in 5 seconds.
- Easing: pass `easing="..."` to `animate`. The default is `"in_out_cubic"` (accelerates then decelerates). Preview all functions in a terminal with:

```bash
textual easing
```

  The preview needs the `textual-dev` package (`pip install textual-dev`).
- Completion callback: pass a callable as `on_complete`; Textual runs it when the animation finishes.
- Delay: pass `delay=` (float seconds). `self.box.styles.animate("opacity", value=0.0, duration=2.0, delay=5.0)` starts after 5 seconds and completes 2 seconds after that.

## Gotchas

- The page lists only `duration`, `speed`, `easing`, `on_complete` and `delay` as parameters beyond the attribute name and `value`; check the API reference for others.

## Verify

The page's example sets `box.styles.animate("opacity", value=0.0, duration=2.0)` on a `Static`; the widget fades out over two seconds and is invisible at opacity 0.0.

## Checked

2026-11-07: every claim was read against the full text of these pages: guide/animation. Nothing needed removing.

Method: documentation only; no commands were run.
