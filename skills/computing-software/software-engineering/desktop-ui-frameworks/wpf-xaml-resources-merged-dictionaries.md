---
id: computing-software.software-engineering.desktop-ui-frameworks.wpf-xaml-resources-merged-dictionaries
name: wpf-xaml-resources-merged-dictionaries
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [wpf-xaml-resources-merged-dictionaries, wpf-xaml, wpf, xaml, dotnet, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Share brushes and styles through ResourceDictionary, MergedDictionaries and Static/DynamicResource."
sources:
  - https://learn.microsoft.com/en-us/dotnet/desktop/wpf/systems/xaml-resources-merged-dictionaries
  - https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/resources-wpf
  - https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/staticresource-markup-extension
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# WPF resources and merged dictionaries

**Goal:** reusable theme resources.

```xml
<Application.Resources>
  <ResourceDictionary>
    <ResourceDictionary.MergedDictionaries>
      <ResourceDictionary Source="Themes/Colors.xaml"/>
      <ResourceDictionary Source="Themes/Buttons.xaml"/>
    </ResourceDictionary.MergedDictionaries>
  </ResourceDictionary>
</Application.Resources>
<Border Background="{DynamicResource PanelBrush}"/>
```

**Gotcha:** A `StaticResource` must not forward-reference a resource defined later in the same XAML file (it is unsupported and costs load time); use `DynamicResource` for values that can change at run time, such as themes.

## Verify
- Swap the Colors dictionary at runtime and DynamicResource consumers update.

## Checked

2026-11-03. Confirmed in the WPF merged resource dictionaries page (`MergedDictionaries`, `Source`), the resources page (StaticResource vs DynamicResource) and the StaticResource markup extension page (forward-reference limit). Removed: the XamlParseException claim and the claim that StaticResource resolves only once, which those pages do not state in that form.

Method: documentation only; no commands were run.
