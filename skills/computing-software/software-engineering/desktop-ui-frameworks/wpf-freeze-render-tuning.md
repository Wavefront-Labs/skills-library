---
id: computing-software.software-engineering.desktop-ui-frameworks.wpf-freeze-render-tuning
name: wpf-freeze-render-tuning
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [wpf-freeze-render-tuning, wpf-performance, wpf, virtualization, performance, dotnet, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Freeze Freezable objects in code or XAML and set BitmapScalingMode to lower WPF render cost."
sources:
  - https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/freezable-objects-overview
  - https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/optimizing-performance-2d-graphics-and-imaging
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# WPF Freezable and rendering tuning

**Goal:** lower render cost.

```csharp
var brush = new SolidColorBrush(Colors.SteelBlue);
if (brush.CanFreeze) brush.Freeze();          // now unmodifiable
RenderOptions.SetBitmapScalingMode(img, BitmapScalingMode.LowQuality);
```

```xml
<!-- xmlns:PresentationOptions="http://schemas.microsoft.com/winfx/2006/xaml/presentation/options"
     mc:Ignorable="PresentationOptions" -->
<SolidColorBrush x:Key="B" Color="SteelBlue" PresentationOptions:Freeze="True"/>
```

**Gotcha:** A frozen object throws `InvalidOperationException` if you modify it, and not every Freezable can be frozen (check `CanFreeze`). Freezing a container freezes the objects it contains. Mark the `PresentationOptions:Freeze` attribute ignorable with `mc:Ignorable` because not every XAML reader recognises it.

## Verify
- Modifying the frozen brush throws, and profiling shows lower UI thread time.

## Checked

2026-11-03. Confirmed in the Freezable objects overview (Freeze, CanFreeze, InvalidOperationException on modification, contained objects frozen, `PresentationOptions:Freeze`, options namespace, mc:Ignorable recommendation) and the 2D graphics and imaging performance page (BitmapScalingMode). Removed: DropShadowEffect and AllowsTransparency advice and the Visual Studio profiler menu path, which are not confirmed by those pages.

Method: documentation only; no commands were run.
