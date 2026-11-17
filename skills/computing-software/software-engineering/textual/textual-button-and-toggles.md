---
id: computing-software.software-engineering.textual.textual-button-and-toggles
name: textual-button-and-toggles
category: computing-software
field: software-engineering
product: textual
tags: [textual, widgets-buttons, button, switch, checkbox, radioset, radiobutton, tui]
level: practitioner
status: docs-checked
description: "Use Textual Button, Switch, Checkbox, RadioButton and RadioSet: variants, value attributes, Pressed and Changed messages, and default bindings."
sources: [https://textual.textualize.io/widgets/button/, https://textual.textualize.io/widgets/switch/, https://textual.textualize.io/widgets/checkbox/, https://textual.textualize.io/widgets/radiobutton/, https://textual.textualize.io/widgets/radioset/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual button and toggle widgets

Goal: collect clicks and boolean or single-choice input.

## Method
- `Button` is pressed by mouse click or Return when focused. Reactives: `label` (str, default `""`), `variant` (`default`, `primary`, `success`, `warning`, `error`; default `"default"`), `disabled` (bool, default `False`; disabled buttons cannot be focused or clicked). Constructor: `Button(label, variant, name=, id=, classes=, disabled=, tooltip=, action=, compact=, flat=)`. Message `Button.Pressed` carries `.button` (alias `.control`); handler `on_button_pressed`.
- `Switch`: reactive `value: bool` (default `False`). Message `Switch.Changed` with `.value` and `.switch`; handler `on_switch_changed`. Enter or Space toggles.
- `Checkbox` (added 0.13.0): reactive `value: bool`, message `Checkbox.Changed`, Enter or Space toggles.
- `RadioButton` (0.13.0): `value: bool`, best used inside a `RadioSet`; `RadioButton("label", value=True)` pre-selects. Label may be a Rich `Text`.
- `RadioSet` (0.13.0, a container that groups `RadioButton`s): holds `RadioButton`s (or plain strings) so only one is on. Message `RadioSet.Changed` has `.pressed` (the RadioButton), `.index`, `.radio_set`; handler `on_radio_set_changed`. Properties `pressed_button` and `pressed_index`. Bindings: Down/Right next, Up/Left previous, Enter/Space toggle.

```python
def on_radio_set_changed(self, event: RadioSet.Changed) -> None:
    self.query_one("#pressed", Label).update(f"Pressed button label: {event.pressed.label}")
```

## Gotchas
- Button spacing comes from its border and `min-width` of 16 columns, not padding: set `border: none;` and adjust `min-width` to remove it.
- To remove spacing around a `Switch`, set `border: none;` and `padding: 0;`.

## Verify
Docs example: in the button demo, clicking a non-disabled button exits the app and prints that button's details to the console.

## Checked

2026-11-07: every claim was read against the full text of these pages: widgets/button, widgets/switch, widgets/checkbox, widgets/radiobutton, widgets/radioset. Removed the claim that RadioSet is not focusable; the page does not say so. Fixed the RadioSet.Changed snippet label text to match the page.

Method: documentation only; no commands were run.
