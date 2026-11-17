---
id: computing-software.software-engineering.desktop-ui-frameworks.wpf-attached-properties
name: wpf-attached-properties
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [wpf-attached-properties, wpf-dependency-properties, wpf, dependency-property, dotnet, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Create attached properties with RegisterAttached and Get/Set accessors for use on other elements."
sources:
  - https://learn.microsoft.com/en-us/dotnet/desktop/wpf/properties/attached-properties-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# WPF attached properties

**Goal:** extend elements without subclassing.

```csharp
public static class Watermark {
    public static readonly DependencyProperty TextProperty =
        DependencyProperty.RegisterAttached("Text", typeof(string), typeof(Watermark),
            new PropertyMetadata(null, OnTextChanged));
    public static string GetText(DependencyObject o) => (string)o.GetValue(TextProperty);
    public static void SetText(DependencyObject o, string v) => o.SetValue(TextProperty, v);
    static void OnTextChanged(DependencyObject d, DependencyPropertyChangedEventArgs e) { /* react to the new value */ }
}
// XAML: <TextBox local:Watermark.Text="Search"/>
```

**Gotcha:** Declare the identifier as a `public static readonly DependencyProperty` field named `<Name>Property` and provide static `Get<Name>`/`Set<Name>` accessors; XAML uses those accessors.

## Verify
- Setting the property in XAML calls the changed callback.

## Checked

2026-11-03. Confirmed in the WPF attached properties overview: `DependencyProperty.RegisterAttached`, the public static readonly identifier field, and static Get/Set accessor methods. Removed: the claim about leaking handlers, which the page does not state.

Method: documentation only; no commands were run.
