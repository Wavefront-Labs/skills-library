---
id: computing-software.software-engineering.desktop-ui-frameworks.wpf-xaml-markup-extensions
name: wpf-xaml-markup-extensions
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [wpf-xaml-markup-extensions, wpf-xaml, wpf, xaml, dotnet, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Map XAML namespaces to CLR namespaces, use x:Static and x:Name, and know namescope limits."
sources:
  - https://learn.microsoft.com/en-us/dotnet/desktop/wpf/xaml/
  - https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/markup-extensions-and-wpf-xaml
  - https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/wpf-xaml-namescopes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# WPF markup extensions and namespaces

**Goal:** clean XAML that references code.

```xml
<Window xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:local="clr-namespace:App;assembly=App">
  <TextBlock Text="{x:Static local:Strings.Title}" x:Name="Header"/>
</Window>
```

**Gotcha:** `x:Static` produces static values from code entities such as static properties and fields. Names declared with `x:Name` live in a XAML namescope: roots such as `Window` and `Page` control one, using the same name twice in a namescope is an error, and names added to the object tree after parsing are not registered automatically (use `RegisterName`).

## Verify
- The XAML designer and build both resolve the namespaces without warnings.

## Checked

2026-11-03. Confirmed in the WPF XAML overview (xmlns and `clr-namespace:...;assembly=...` mapping), the markup extensions page (`x:Static`) and the XAML namescopes page (root namescopes, duplicate names, `RegisterName`). Removed: the DataContext element-in-XAML sample, the custom MarkupExtension class claim from the description, and the templates/field claim about x:Name, which those pages did not confirm.

Method: documentation only; no commands were run.
