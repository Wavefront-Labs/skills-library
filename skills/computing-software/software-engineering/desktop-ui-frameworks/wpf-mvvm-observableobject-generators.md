---
id: computing-software.software-engineering.desktop-ui-frameworks.wpf-mvvm-observableobject-generators
name: wpf-mvvm-observableobject-generators
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [wpf-mvvm-observableobject-generators, wpf-mvvm, wpf, mvvm, communitytoolkit, dotnet, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Generate observable properties from fields with [ObservableProperty] in partial classes."
sources:
  - https://learn.microsoft.com/en-us/dotnet/communitytoolkit/mvvm/generators/observableproperty
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CommunityToolkit.Mvvm ObservableProperty

**Goal:** minimal-boilerplate view models.

```csharp
using CommunityToolkit.Mvvm.ComponentModel;
public partial class MainViewModel : ObservableObject
{
    [ObservableProperty]
    [NotifyPropertyChangedFor(nameof(FullName))]
    private string first = "";

    [ObservableProperty]
    private string last = "";

    public string FullName => $"{First} {Last}";
    partial void OnFirstChanged(string value) { /* react */ }
}
```

**Gotcha:** The annotated fields must be in a `partial` class with the INotifyPropertyChanged infrastructure (for example deriving `ObservableObject`). The generator expects field names like `lowerCamel`, `_lowerCamel` or `m_lowerCamel` and produces an `UpperCamel` property. Optional `partial void On<Name>Changing/Changed` methods are generated for each property.

## Verify
- The project builds and `Binding First` updates the view.

## Checked

2026-11-03. Confirmed in the MVVM Toolkit ObservableProperty generator page: partial class requirement, field-name to property-name rule, `NotifyPropertyChangedFor`, and the `OnNameChanged(value)` partial methods. Removed: the `dotnet add package` line and the claim that the build has no warnings.

Method: documentation only; no commands were run.
