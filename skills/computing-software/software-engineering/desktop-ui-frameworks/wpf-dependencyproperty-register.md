---
id: computing-software.software-engineering.desktop-ui-frameworks.wpf-dependencyproperty-register
name: wpf-dependencyproperty-register
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [wpf-dependencyproperty-register, wpf-dependency-properties, wpf, dependency-property, dotnet, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Declare a DependencyProperty with a CLR wrapper and a property-changed callback in metadata."
sources:
  - https://learn.microsoft.com/en-us/dotnet/desktop/wpf/properties/custom-dependency-properties
  - https://learn.microsoft.com/en-us/dotnet/desktop/wpf/properties/dependency-property-value-precedence
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Register a WPF dependency property

**Goal:** bindable, styleable custom control property.

```csharp
public static readonly DependencyProperty ValueProperty =
    DependencyProperty.Register(nameof(Value), typeof(double), typeof(Gauge),
        new PropertyMetadata(0.0, OnValueChanged));
public double Value { get => (double)GetValue(ValueProperty); set => SetValue(ValueProperty, value); }
static void OnValueChanged(DependencyObject d, DependencyPropertyChangedEventArgs e) => ((Gauge)d).UpdateNeedle();
```

**Gotcha:** The CLR wrapper is only a convenience for code: keep it to `GetValue`/`SetValue` and put reaction logic in the property-changed callback in metadata, which the property system invokes whenever the value changes (including changes made by styles). A coercion callback, when used, sits at the top of the value precedence order.

## Verify
- Binding to Value works two-way and the property can be set from a Style.

## Checked

2026-11-03. Confirmed in the WPF custom dependency properties and value precedence pages: CLR wrapper with get/set, change callback in property metadata invoked on every change, property system coercion has the highest precedence. Removed: FrameworkPropertyMetadataOptions.AffectsRender, the CoerceValue sample with Math.Clamp, and the claim that XAML and bindings bypass the wrapper, which those pages did not confirm.

Method: documentation only; no commands were run.
