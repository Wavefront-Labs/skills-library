---
id: computing-software.software-engineering.desktop-ui-frameworks.wpf-binding-modes-and-updatesourcetrigger
name: wpf-binding-modes-and-updatesourcetrigger
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [wpf-binding-modes-and-updatesourcetrigger, wpf-data-binding, wpf, binding, dotnet, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Pick OneWay, TwoWay and OneWayToSource binding modes and the UpdateSourceTrigger values."
sources:
  - https://learn.microsoft.com/en-us/dotnet/desktop/wpf/data/
  - https://learn.microsoft.com/en-us/dotnet/desktop/wpf/data/binding-declarations-overview
  - https://learn.microsoft.com/en-us/dotnet/desktop/wpf/data/how-to-control-when-the-textbox-text-updates-the-source
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# WPF binding modes and UpdateSourceTrigger

**Goal:** correct two-way editing.

```xml
<TextBox Text="{Binding Name, Mode=TwoWay, UpdateSourceTrigger=PropertyChanged}"/>
<TextBox Text="{Binding Notes, UpdateSourceTrigger=Explicit}" x:Name="notesBox"/>
<TextBlock Text="{Binding Total, StringFormat=C0}"/>
<Slider Value="{Binding Volume, Mode=OneWayToSource}"/>
```

**Gotcha:** `TextBox.Text` defaults to `LostFocus`, so a Save button can read stale data; use `PropertyChanged` for per-keystroke updates (every validation rule then runs on every keystroke). With `Explicit` the source changes only when code calls `BindingExpression.UpdateSource`, which suits an OK/Cancel dialog. Most other properties default to `PropertyChanged`.

## Verify
- Typing updates the view model without leaving the box.

## Checked

2026-11-03. Confirmed in the WPF data binding overview, binding declarations overview and the TextBox UpdateSourceTrigger how-to: OneWayToSource, TwoWay, `UpdateSourceTrigger` values `LostFocus` (TextBox.Text default), `PropertyChanged` and `Explicit`, `BindingExpression.UpdateSource`, StringFormat use in binding snippets. Removed: `Delay`, `ValidatesOnNotifyDataErrors` and `FallbackValue` usage, which those pages do not cover.

Method: documentation only; no commands were run.
