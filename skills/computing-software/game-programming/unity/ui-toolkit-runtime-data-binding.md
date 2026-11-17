---
id: computing-software.game-programming.unity.ui-toolkit-runtime-data-binding
name: ui-toolkit-runtime-data-binding
category: computing-software
field: game-programming
product: unity
tags: [unity, ui-toolkit-data-binding, ui-toolkit, data-binding, mvvm, game-programming]
level: practitioner
status: draft
description: "Bind Unity 6 UI Toolkit elements to C# data sources at runtime with dataSource, DataBinding paths, CreateProperty, change tracking and converters instead of manual updates."
sources: ["https://docs.unity3d.com/Manual/UIE-runtime-binding.html", "https://docs.unity3d.com/Manual/UIE-runtime-binding-define-data-source.html", "https://docs.unity3d.com/Manual/UIE-runtime-binding-types.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# UI Toolkit runtime data binding

**Goal:** HUD labels and bars update from a model object without per-frame `label.text =` code.

## Data source
```csharp
using System;
using System.Runtime.CompilerServices;
using Unity.Properties;
using UnityEngine.UIElements;
public class PlayerHud : IDataSourceViewHashProvider, INotifyBindablePropertyChanged {
    int health; long version;
    [CreateProperty] public int Health {
        get => health;
        set { if (health == value) return; health = value; version++; Notify(); }
    }
    [CreateProperty] public float HealthPct => health / 100f;
    public event EventHandler<BindablePropertyChangedEventArgs> propertyChanged;
    void Notify([CallerMemberName] string p = "") => propertyChanged?.Invoke(this, new(p));
    public long GetViewHashCode() => version;
}
```
`[CreateProperty]` is mandatory to make a property bindable; Unity's page says fields and properties of user-defined components and ScriptableObjects work as sources. Whether property bags avoid reflection entirely was not checked here.

## Bind
UXML (UI Builder: right-click a field > Add binding):
```xml
<ui:Label text="--">
  <Bindings><ui:DataBinding property="text" data-source-path="Health" binding-mode="ToTarget"/></Bindings>
</ui:Label>
```
Code:
```csharp
root.dataSource = hud;   // inherited by children
label.SetBinding("text", new DataBinding { dataSourcePath = new PropertyPath(nameof(PlayerHud.Health)),
    bindingMode = BindingMode.ToTarget });
```

## Update cost
`BindingUpdateTrigger` has three values: `WhenDirty` (only after `MarkDirty`), `OnSourceChanged` (when a source change is detected, or marked dirty) and `EveryUpdate`. Custom bindings update every frame by default; the default for the built-in `DataBinding` was not confirmed, so set `updateTrigger` explicitly. Implement `IDataSourceViewHashProvider` (cheap version number) and/or `INotifyBindablePropertyChanged` (report with `NotifyPropertyChanged`) so source changes are detectable. Not confirmed here: the exact role of each interface.

## Converters
Register a converter group (`ConverterGroups.RegisterConverterGroup`) to format int to "HP 42" or map
float to style colour; reference by name in UXML `source-to-ui-converters` (converter API names unconfirmed, see Unity's "Convert data types" page).

## Gotchas
- This is the Unity 6 runtime system; editor `SerializedObject` binding (`bindingPath`) is separate.
- Binding to a field without `[CreateProperty]` silently fails; check the UI Builder binding warnings.
- `TwoWay` on text fields writes back on every keystroke; validate in the setter.

## Verify
- [ ] Changing the model updates the UI with no manual refresh code.
- [ ] Profiler shows binding cost near zero when the model is unchanged.
