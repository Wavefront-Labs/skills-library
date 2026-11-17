---
id: computing-software.software-engineering.desktop-ui-frameworks.wpf-datatemplate-selectors
name: wpf-datatemplate-selectors
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [wpf-datatemplate-selectors, wpf-templates-styles, wpf, controltemplate, datatemplate, dotnet, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Render view models with implicit DataTemplates chosen by DataType."
sources:
  - https://learn.microsoft.com/en-us/dotnet/desktop/wpf/data/data-templating-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# WPF DataTemplate and selectors

**Goal:** type-driven UI.

```xml
<Window.Resources>
  <DataTemplate DataType="{x:Type vm:CustomerVm}"><views:CustomerView/></DataTemplate>
  <DataTemplate DataType="{x:Type vm:OrderVm}"><views:OrderView/></DataTemplate>
</Window.Resources>
<ContentControl Content="{Binding Current}"/>
```

**Gotcha:** A `DataTemplate` with a `DataType` is applied automatically to objects of that type, and its `x:Key` is set implicitly; assigning your own `x:Key` overrides that and disables the automatic use. `DataType` is especially useful with a `CompositeCollection` of different object types.
## Verify
- Changing Current swaps the view without code-behind.

## Checked

2026-11-03. Confirmed in the WPF data templating overview: `DataTemplate.DataType` behaves like `Style.TargetType`, applies automatically, implicit `x:Key`, CompositeCollection use. Removed: the claim that implicit templates match the exact runtime type only, and the DataTemplateSelector/ItemTemplateSelector example, which that page excerpt did not confirm.

Method: documentation only; no commands were run.
