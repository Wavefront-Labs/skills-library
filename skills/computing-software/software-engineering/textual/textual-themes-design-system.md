---
id: computing-software.software-engineering.textual.textual-themes-design-system
name: textual-themes-design-system
category: computing-software
field: software-engineering
product: textual
tags: [textual, design-themes, theme, design-variables, shades, register-theme, base-colors, css-variables]
level: practitioner
status: docs-checked
description: "Register and apply Textual themes, use base color and shade CSS variables, override theme variables, and add app-specific variables."
sources: [https://textual.textualize.io/guide/design/]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Textual themes and design system

Goal: build a custom theme and style widgets with theme variables so they follow theme changes.

## Method

1. Switch themes at runtime through the Command Palette (ctrl+p), or in code by name with `self.theme = "nord"`. A theme must be registered first; built-in themes already are.
2. Define a theme (only `primary` is required; Textual attempts to generate the other base colors if omitted):

```python
from textual.theme import Theme

arctic_theme = Theme(
    name="arctic",
    primary="#88C0D0",
    secondary="#81A1C1",
    accent="#B48EAD",
    foreground="#D8DEE9",
    background="#2E3440",
    success="#A3BE8C",
    warning="#EBCB8B",
    error="#BF616A",
    surface="#3B4252",
    panel="#434C5E",
    dark=True,
    variables={
        "block-cursor-text-style": "none",
        "footer-key-foreground": "#88C0D0",
        "input-selection-background": "#81a1c1 35%",
    },
)
```

3. Register in `on_mount`, then set it:

```python
def on_mount(self) -> None:
    self.register_theme(arctic_theme)
    self.theme = "arctic"
```

4. Use variables in CSS: `MyWidget { background: $primary; color: $foreground; }`. They update when the theme changes.

Base colors: `$primary`, `$secondary`, `$foreground`, `$background`, `$surface`, `$panel`, `$boost`, `$warning`, `$error`, `$success`, `$accent`.

Shades: append `-lighten-1`..`-lighten-3` or `-darken-1`..`-darken-3` (e.g. `$secondary-darken-1`, `$error-lighten-3`).

Text: `$text`, `$text-muted`, `$text-disabled` stay legible on any background; `$foreground-muted`, `$foreground-disabled`; colored `$text-primary`, `$text-secondary`, `$text-accent`, `$text-warning`, `$text-error`, `$text-success`. Muted backgrounds (base color blended with `$background` at 70%): `$primary-muted`, `$secondary-muted`, `$accent-muted`, `$warning-muted`, `$error-muted`, `$success-muted`.

`variables={...}` overrides framework variables such as `$border`, `$scrollbar`, `$link-color`, `$footer-key-foreground`, `$button-foreground`.

App-specific variables: override `App.get_theme_variable_defaults` to return a dict of names and defaults; a theme's `variables` value wins.

## Gotchas

- `dark=True/False` on `Theme` influences how variables are generated and how built-in widgets look.
- Setting `self.theme` refreshes the app immediately.
- Preview the colour system with `textual colors` on the command line; switch theme there via ctrl+p to see base variables and shades.

## Checked
2026-11-07. Read in full: Themes guide (guide/design). Confirmed: ctrl+p and App.theme, Theme constructor, register_theme, only primary required, base colours, shades, text and muted variables, variables override, get_theme_variable_defaults, dark argument, textual colors. Reworded: other base colours are generated on a best-effort basis. Moved: the textual colors preview into Gotchas; removed the Verify section.
Method: documentation only; no commands were run.
