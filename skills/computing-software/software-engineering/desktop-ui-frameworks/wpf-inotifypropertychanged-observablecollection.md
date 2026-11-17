---
id: computing-software.software-engineering.desktop-ui-frameworks.wpf-inotifypropertychanged-observablecollection
name: wpf-inotifypropertychanged-observablecollection
category: computing-software
field: software-engineering
product: desktop-ui-frameworks
tags: [wpf-inotifypropertychanged-observablecollection, wpf-data-binding, wpf, binding, dotnet, desktop-ui-frameworks]
level: practitioner
status: docs-checked
description: "Implement INotifyPropertyChanged and use ObservableCollection for bound lists."
sources:
  - https://learn.microsoft.com/en-us/dotnet/desktop/wpf/data/
  - https://learn.microsoft.com/en-us/dotnet/desktop/wpf/data/binding-sources-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# INotifyPropertyChanged and ObservableCollection

**Goal:** views that update.

```csharp
public class Person : INotifyPropertyChanged {
    string _name = "";
    public string Name { get => _name; set { if (_name != value) { _name = value; PropertyChanged?.Invoke(this, new(nameof(Name))); } } }
    public event PropertyChangedEventHandler? PropertyChanged;
}
public ObservableCollection<Person> People { get; } = new();
```

**Gotcha:** For OneWay and TwoWay bindings the source must signal changes: implement `INotifyPropertyChanged` (the recommended mechanism) for properties, and use `ObservableCollection<T>` (which exposes `INotifyCollectionChanged`) for collections.

## Verify
- Adding an item at runtime appears in the ListBox without refresh.

## Checked

2026-11-03. Confirmed in the WPF data binding overview and binding sources overview: INotifyPropertyChanged as the recommended change-notification mechanism, `ObservableCollection<T>` exposing INotifyCollectionChanged, and the need for notifications on OneWay/TwoWay bindings. Removed: the cross-thread CollectionChanged claim and BindingOperations.EnableCollectionSynchronization, which those pages do not cover.

Method: documentation only; no commands were run.
