---
id: computing-software.software-engineering.textual.textual-progress-widgets
name: textual-progress-widgets
category: computing-software
field: software-engineering
product: textual
tags: [textual, widgets-progress, progress-bar, loading-indicator, sparkline, gradient, tui]
level: practitioner
status: docs-checked
description: "Show progress in Textual with ProgressBar (total, advance, gradient), LoadingIndicator and the loading reactive, and Sparkline (data, summary_function, colors)."
sources: [https://textual.textualize.io/widgets/progress_bar/, https://textual.textualize.io/widgets/loading_indicator/, https://textual.textualize.io/widgets/sparkline/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual ProgressBar, LoadingIndicator and Sparkline

Goal: communicate progress, waiting and trends.

## Method
**ProgressBar**: reactives `total` (float or None), `progress` (default 0) and read-only `percentage` (None until `total` is set). With no total it shows the indeterminate state.
- Constructor options: `ProgressBar(total=100, show_eta=False)`, plus `show_bar`, `show_percentage`, `gradient`. The docs hide the ETA when the task is not one continuous, uninterrupted run.
- Update with `bar.advance(10)` or `bar.update(total=200, progress=50)` (`update` also takes `advance=`).
- Gradient: set a `Gradient` object on the ProgressBar for a smooth bar; this overrides CSS styles.
- Styling: three sub-widgets: `Bar` (`#bar`), `PercentageStatus` (`#percentage`) and `ETAStatus` (`#eta`), the last two being Labels. Bar component classes: `bar--bar`, `bar--complete`, `bar--indeterminate`.
- Posts no messages.

**LoadingIndicator** (0.15.0+): pulsating dots for loading data; set colour with CSS `LoadingIndicator { color: red; }`. Widgets also have a `loading` reactive that temporarily replaces the widget with a LoadingIndicator. No messages.

**Sparkline** (0.27.0+): reactives `data` (`Sequence[float]` or None) and `summary_function` (default `max`). Data is split into equal chunks, one bar per chunk, and the sparkline width sets the number of bars (width 3 with 12 points gives 3 bars of 4 points). Each bar is the summary of its chunk: `max`, `min`, or a mean function. Colours come from component classes `sparkline--max-color` and `sparkline--min-color`.

```python
self.query_one(ProgressBar).advance(10)
```

## Checked
2026-11-07. Read in full: ProgressBar, LoadingIndicator and Sparkline widget pages. Confirmed: reactives and defaults, constructor options, advance/update, gradient overriding CSS, sub-widget ids, bar component classes, no messages, 0.15.0 and 0.27.0 badges, Sparkline chunking example (2, 4, 8 with max), summary_function and colour component classes. Removed: the not-focusable claim (page prints only a generic bullet), the source-code attributions and the Verify section.
Method: documentation only; no commands were run.
