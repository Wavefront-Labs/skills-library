---
id: computing-software.software-engineering.textual.textual-input-widgets
name: textual-input-widgets
category: computing-software
field: software-engineering
product: textual
tags: [textual, widgets-text-input, input, masked-input, text-area, validators, tui]
level: practitioner
status: docs-checked
description: "Use Textual Input (type, restrict, max_length, validators), MaskedInput template masks, and TextArea (language, selection, themes, tab behaviour, undo, read-only)."
sources: [https://textual.textualize.io/widgets/input/, https://textual.textualize.io/widgets/masked_input/, https://textual.textualize.io/widgets/text_area/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual Input, MaskedInput and TextArea

Goal: collect and validate typed text.

## Method
**Input** (single line). Reactives: `value`, `cursor_position`, `placeholder`, `password`, `restrict` (regex), `type`, `max_length`, `valid_empty`, `cursor_blink`.
- `type`: `"integer"`, `"number"` or `"text"` (default); non-text types add the matching validator.
- `restrict=r"[01]*"` blocks characters that would stop the whole value matching. `max_length` > 0 caps length.
- `validators=[...]` (built-ins such as `Number`, `Function`, or subclass `Validator` and report via `self.failure(...)`). Validation runs on change, submit and blur; limit it with `validate_on=["submitted"]`. Any failing validator fails the input. Read `event.validation_result` in `Input.Changed`, `Input.Submitted` or `Input.Blurred`. Failed inputs get the `-invalid` class (red border by default); style `-valid` yourself. `valid_empty=True` lets empty values bypass validators.

**MaskedInput** (0.80.0+, derived from Input): reactive `template`. Template length is the max length. Mask characters: `A`/`a` letter (required/optional), `N`/`n` alphanumeric, `X`/`x` any non-space, `9`/`0` digit, `D`/`d` digit 1-9, `#` one of 0-9 + -, `H`/`h` hex, `B`/`b` binary. `>` uppercases following input, `<` lowercases, `!` disables conversion. Other characters are separators inserted automatically; escape with a backslash. End the mask with `;c` to choose placeholder character `c`.

**TextArea** (0.38.0+, soft wrap 0.48.0+): multi-line. `TextArea.code_editor(...)` returns soft-wrap off, line numbers on, Tab inserting a tab character.
- Highlighting: `pip install "textual[syntax]"`, then set `language` (e.g. `"python"`, `"markdown"`).
- Content: `text`, `selected_text`, `get_text_range`, `replace`, `insert`, `delete`, `clear`; `document.end` is the end location.
- Cursor: `cursor_location` is `(row, column)`, zero-based. `selection = Selection(start=(0, 0), end=(2, 0))`; `move_cursor((4, 8), select=True)`; F6 select line, F7 select all.
- Themes: default `css`; builtin `dracula`, `github_light`, `monokai`, `vscode_dark`; set `theme=`; custom via `TextAreaTheme(...)` plus `register_theme`.
- Tab moves focus by default; `tab_behavior="indent"` inserts a tab and Escape moves focus. `indent_type` and `indent_width` (default 4).
- Ctrl+Z undo, Ctrl+Y redo; `max_checkpoints` limits history. `read_only=True` blocks user edits only and adds `-read-only` class. `show_line_numbers`, `line_number_start`.
- Messages: `TextArea.Changed`, `TextArea.SelectionChanged`.

## Gotchas
- `restrict` matches the full value, not just the new character.
- Input and TextArea show a border or outline; set `border: none;` (and `padding: 0;` for TextArea) to remove it.

## Verify
Docs example: `Input(type="integer")` rejects non-digit keys; `text_area.cursor_location` starts at `(0, 0)`.

## Checked

2026-11-07: every claim was read against the full text of these pages: widgets/input, widgets/masked_input, widgets/text_area. Nothing needed removing.

Method: documentation only; no commands were run.
