---
id: computing-software.software-engineering.textual.textual-selection-widgets
name: textual-selection-widgets
category: computing-software
field: software-engineering
product: textual
tags: [textual, widgets-selection, select, selection-list, option-list, tui]
level: practitioner
status: docs-checked
description: "Choose between Textual Select, SelectionList and OptionList: how options are built, value and highlighted attributes, blank state, and the messages each posts."
sources: [https://textual.textualize.io/widgets/select/, https://textual.textualize.io/widgets/selection_list/, https://textual.textualize.io/widgets/option_list/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual Select, SelectionList and OptionList

Goal: pick the right list-style widget and wire its messages.

## Method
**Select** (0.24.0+): compact drop-down. Options are `(display, value)` tuples (display may be a Rich renderable) passed to the constructor, set later with `set_options`, or built with the `from_values` class method.
- `value` holds the current option value (also on `Select.Changed`); reactive `expanded` (default `False`).
- `allow_blank=True` permits no selection; `value` is then `Select.NULL`. `Select.is_blank` checks it, `Select.clear` sets it.
- `type_to_search` (default on) moves the cursor to a matching option while expanded; set `False` to disable.
- Typing is optional: `my_select: Select[int] = Select([("First", 1), ("Second", 2)])`.
- Message: `Select.Changed`.

**SelectionList** (0.27.0+): vertical list of checkable items with single-line prompts (may be Rich `Text`) and unique values. Build with tuples `(prompt, value)` or `(prompt, value, initial_selected)`, or with `Selection` objects; `SelectionList(*selections)`. Typed generic: `SelectionList[int]`.
- Reactive `highlighted` (`int | None`, default `None`).
- Messages: `SelectionList.SelectedChanged` (use this to react to the set of selected values), `SelectionToggled`, `SelectionHighlighted`.
- Inherits `OptionList` bindings and component classes.

**OptionList** (0.17.0+): vertical list of Rich renderable options, so options can be any height (e.g. Rich tables). Build from plain strings, or `Option` instances for ids and initial disabled state; `Separator` adds separator lines.
- Reactive `highlighted` (`int | None`, default `None`).
- Messages: `OptionList.OptionHighlighted` and `OptionList.OptionSelected`, both inheriting `OptionList.OptionMessage`.

## Gotchas
- Select value may be `Select.NULL` when blank is allowed, so compare before using it as your own data type.

## Checked
2026-11-07. Read in full: Select and SelectionList pages; OptionList page read through its examples, reactive attributes, messages, bindings and parameters. Confirmed: version badges, option tuple form, set_options/from_values, allow_blank and Select.NULL/is_blank/clear, type_to_search, expanded, highlighted defaults, message names, tuple and Selection forms, SelectedChanged guidance, Option ids and disabled, Separator, OptionList.OptionMessage base. Removed: the Verify section.
Method: documentation only; no commands were run.
