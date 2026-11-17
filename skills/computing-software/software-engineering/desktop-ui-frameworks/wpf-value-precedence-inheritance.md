---
id: computing-software.software-engineering.desktop-ui-frameworks.wpf-value-precedence-inheritance
name: wpf-value-precedence-inheritance
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [wpf-value-precedence-inheritance, wpf-dependency-properties, wpf, dependency-property, dotnet, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Predict which WPF dependency property value wins, and set values with SetCurrentValue."
sources:
  - https://learn.microsoft.com/en-us/dotnet/desktop/wpf/properties/dependency-property-value-precedence
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# WPF dependency property value precedence

**Goal:** predict which value wins.

```csharp
// precedence, highest first (excerpt): property system coercion, active animations, local values,
// ..., style triggers, template triggers, ..., inheritance, default from metadata
textBox.SetCurrentValue(TextBox.TextProperty, "x");   // keeps the source of the previous value
var src = DependencyPropertyHelper.GetValueSource(textBox, TextBox.TextProperty);
Debug.WriteLine(src.BaseValueSource);
```

**Gotcha:** A local value set in code replaces a binding or dynamic resource on that property, and `ClearValue` does not restore it. `SetCurrentValue` is outside the precedence list: it changes the value without overwriting the source of the previous value, so a later trigger action can set the trigger value again. Use it inside controls.

## Verify
- BaseValueSource reports the source you expect.

## Checked

2026-11-03. Confirmed in the WPF dependency property value precedence page: the ordered list (coercion first, animations, local values, style triggers, template triggers, inheritance, metadata default), `SetCurrentValue` semantics, `GetValueSource`, and the binding/dynamic-resource replacement and `ClearValue` caveat. Removed: the abbreviated "template/style triggers > style setter" ordering from the draft (use the page's full list) and the TextBox ClearValue example.

Method: documentation only; no commands were run.
