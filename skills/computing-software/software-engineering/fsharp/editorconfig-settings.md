---
id: computing-software.software-engineering.fsharp.editorconfig-settings
name: editorconfig-settings
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, editorconfig-settings, fsharp-format-tools, editorconfig, fantomas-settings]
level: practitioner
status: draft
description: "Configure Fantomas and editor behaviour in .editorconfig with indent size, line length and bracket style."
sources:
  - https://fsprojects.github.io/fantomas/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# .editorconfig for F#
**Goal:** project-wide formatting rules.

```ini
root = true

[*.{fs,fsx,fsi}]
indent_style = space
indent_size = 4
max_line_length = 120
end_of_line = lf
insert_final_newline = true
fsharp_multiline_bracket_style = aligned
fsharp_space_before_uppercase_invocation = false
```
- Standard keys: `indent_size`, `indent_style`, `max_line_length`, `end_of_line`, `insert_final_newline`.
- Fantomas-specific keys start with `fsharp_` (for example `fsharp_multiline_bracket_style` with values like `cramped`, `aligned`, `stroustrup`; check the Fantomas settings doc for your version, since options differ between releases).
- The nearest `.editorconfig` upward from each file wins; `root = true` stops the search.
- Keep options near defaults; the F# community expects the default look.

## Gotchas
- Unknown `fsharp_` keys are ignored silently.
- Changing settings reformats the entire codebase and creates large diffs.

## Self-check
Change `indent_size` to 2 temporarily, run Fantomas on one file, and observe the difference.
