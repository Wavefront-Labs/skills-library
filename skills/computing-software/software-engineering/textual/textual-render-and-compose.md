---
id: computing-software.software-engineering.textual.textual-render-and-compose
name: textual-render-and-compose
category: computing-software
field: software-engineering
product: textual
tags: [textual, render, compose, custom-widget, rich, compound-widget, background, widgets]
level: practitioner
status: docs-checked
description: "Decide between Textual widget render and compose methods, and combine both so render supplies a background beneath composed child widgets."
sources: [https://textual.textualize.io/how-to/render-and-compose/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Render versus compose in a Textual widget

Goal: know which method defines what a custom widget looks like.

## Method

1. `render()` returns a Rich renderable, anything you could print with Rich. The simplest is a string; it could also be a Rich `Text`, a `Table`, or something from a third-party library. Textual combines the result with the widget's CSS styles and displays it within the widget's borders.
2. `compose()` builds a compound widget (a widget made of other widgets) by yielding child widgets.
3. Rule of thumb: if you implement `compose`, you do not need `render`, because the yielded widgets define the appearance.
4. You can implement both. Then `render` sets the widget's background and `compose` adds widgets on top of it.
5. The worked example is a `Splash` widget: `compose` yields a single `Static` with a message, while `render` returns a `LinearGradient` (from `textual.renderables.gradient`) as the background. It refreshes 30 times a second so the gradient animates.

Summary from the page:

1. Use `render` to return simple text or a Rich renderable.
2. Use `compose` to create a widget out of other widgets.
3. If you define both, `render` is used as a background.

## Gotchas

- The two are easy to confuse because both define appearance; they have different purposes.
- Animated gradients can distract in real apps.

## Checked
2026-11-07. Read in full: Render and compose how-to. Confirmed: render returns a Rich renderable combined with CSS styles, compose builds compound widgets, rule of thumb, render as background beneath composed widgets, the Splash example with LinearGradient and a 1/30 auto_refresh, the summary and the animation tip. Removed: the Verify section.
Method: documentation only; no commands were run.
