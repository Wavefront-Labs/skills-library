---
id: computing-software.software-engineering.desktop-ui-frameworks.wpf-ui-virtualization
name: wpf-ui-virtualization
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [wpf-ui-virtualization, wpf-performance, wpf, virtualization, performance, dotnet, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Keep large WPF lists fast with UI virtualization, container recycling and deferred scrolling."
sources:
  - https://learn.microsoft.com/en-us/dotnet/desktop/wpf/advanced/optimizing-performance-controls
  - https://learn.microsoft.com/en-us/dotnet/desktop/wpf/controls/how-to-improve-the-scrolling-performance-of-a-listbox
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# WPF UI virtualization

**Goal:** smooth large lists.

```xml
<ListView ItemsSource="{Binding Rows}"
          VirtualizingStackPanel.IsVirtualizing="True"
          VirtualizingStackPanel.VirtualizationMode="Recycling"
          ScrollViewer.IsDeferredScrollingEnabled="True"/>
```

**Gotcha:** UI virtualization is on by default for `ListView` and `ListBox` bound to data, and it is lost when item containers are added directly to the control, when containers are of different types, when `ScrollViewer.CanContentScroll` is false, or when `IsVirtualizing` is false. Container recycling reuses containers for different data items, so state kept on a container (for example an Expander's `IsExpanded`) must be saved with the item. No built-in WPF control offers data virtualization.

## Verify
- Only containers for visible rows exist for a very large list.

## Checked

2026-11-03. Confirmed in the WPF optimizing performance: controls page: default virtualization for ListView/ListBox, the conditions that disable it, container recycling (`VirtualizingStackPanel.VirtualizationMode`), container state caveat, deferred scrolling via `ScrollViewer.IsDeferredScrollingEnabled`, no built-in data virtualization. Removed: the 100k-item figure, IsContainerVirtualizable, ScrollUnit, the ScrollViewer wrapper/StackPanel ItemsPanel/IsVirtualizingWhenGrouping claims and the Live Visual Tree check, which that page does not cover.

Method: documentation only; no commands were run.
