---
id: computing-software.software-engineering.textual.textual-design-a-layout
name: textual-design-a-layout
category: computing-software
field: software-engineering
product: textual
tags: [textual, design-layout, containers, fr-units, dock, placeholder, sketch, tcss]
level: practitioner
status: docs-checked
description: "Turn a sketch into a Textual layout working outside in with Placeholder widgets, dock for fixed bars, fr units for flexible space and scrolling containers."
sources: [https://textual.textualize.io/how-to/design-a-layout/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Designing a Textual layout

Goal: go from a rough sketch to a working screen structure before writing real widgets.

## Method

1. Sketch first (pen and paper is fine): a rectangle for the terminal, a rectangle per element, annotated with its content and whether and which way it scrolls.
2. Work outside in. Add fixed outer elements (header, footer, sidebar) first. Use `Placeholder` widgets (subclass it, or pass an id which it displays) to visualise the design before real content exists. Real apps can use the builtin `Header` and `Footer`.
3. Dock fixed widgets with the `dock` rule so they stick to an edge and have limited height. Inline CSS in Python goes in the `DEFAULT_CSS` class variable; docking a widget reduces the area available to the others, and Textual compensates automatically.
4. Give flexible regions `width: 1fr;` and `height: 1fr;` so they take whatever space remains; with one such widget it fills all remaining space. A border helps show dimensions.
5. Prefer a builtin container over a styled Placeholder: containers already use `fr` units, so no extra CSS is needed. Use `HorizontalScroll` for a row of columns (adds a horizontal scrollbar) and subclass `VerticalScroll` for each column (vertical scrollbar).
6. A container child has a width of `1fr` by default, so four columns each take a quarter of the screen. For fixed-width columns set the width (the example uses 32) and give items a fixed height (the example uses 5) or `auto` to fit content.
7. Replace placeholders with builtin or custom widgets.

## Gotchas

- A container looks like blank space until children are added.

## Verify

Run the app: header and footer stay fixed top and bottom, the middle region resizes with the terminal, and columns scroll independently.

## Checked

2026-11-07: every claim was read against the full text of these pages: how-to/design-a-layout. Nothing needed removing.

Method: documentation only; no commands were run.
