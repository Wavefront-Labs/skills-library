---
id: computing-software.game-programming.godot.csharp-signals-and-exports
name: csharp-signals-and-exports
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, csharp, dotnet, csharp-signals, export-attribute, partial-classes, source-generators, game-programming]
level: practitioner
status: docs-checked
description: "Declare signals and exported properties in Godot 4 C#: [Signal] delegates with EventHandler suffix, EmitSignal and C# events, [Export] variants, and source-generator requirements."
sources: ["https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/c_sharp_signals.html", "https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/c_sharp_exports.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# C# signals and exports

**Goal:** idiomatic Godot 4 C# scripts whose signals and exports work in the editor and from GDScript.

## Class shape
```csharp
using Godot;

public partial class Health : Node          // partial is required: source generators add members
{
    [Signal] public delegate void HealthChangedEventHandler(int current, int max);
    [Signal] public delegate void DiedEventHandler();

    [Export] public int MaxHealth { get; set; } = 100;
    [Export(PropertyHint.Range, "0,10,0.1")] public float Regen { get; set; } = 1f;
    [Export] public PackedScene DeathFx { get; set; }
    [Export] public Node3D Target { get; set; }
    [ExportGroup("Resistances")] [Export] public float FireResist { get; set; }

    private int _current;
    public void Damage(int amount)
    {
        _current = Mathf.Max(0, _current - amount);
        EmitSignal(SignalName.HealthChanged, _current, MaxHealth);
        if (_current == 0) EmitSignal(SignalName.Died);
    }
}
```
- Signal delegates **must end in `EventHandler`**; the signal name drops the suffix (`HealthChanged`).
- Use generated `SignalName.X`, `PropertyName.X`, `MethodName.X` constants instead of strings.
- Exports work on fields or properties; the class must be `partial`.

## Connecting
```csharp
health.HealthChanged += OnHealthChanged;              // generated C# event: typed, fast
health.Died += () => QueueFree();
// Disconnect: health.HealthChanged -= OnHealthChanged;  (do it in _ExitTree for long-lived emitters)

button.Pressed += OnPressed;                           // built-in signals are also C# events
health.Connect(Health.SignalName.Died, Callable.From(OnDied), (uint)ConnectFlags.OneShot);   // when flags are needed
```
- C# event subscriptions are tracked by Godot and auto-disconnected when the target node is freed for
  methods on GodotObjects; lambdas capturing other objects may still leak; unsubscribe explicitly.
- Signal argument types must be Variant-compatible (primitives, Godot types, GodotObject subclasses).

## Export notes
- `[Export(PropertyHint.Enum, "Melee,Ranged")]`, `[Export] public MyEnum Kind` (C# enums show as dropdown),
  `[Export] public Godot.Collections.Array<PackedScene> Drops` (use Godot collections for exports, not `List<T>`).
- `[ExportCategory]`, `[ExportGroup]`, `[ExportSubgroup]`; `[Tool]` attribute for editor execution.

## Verify
- [ ] Signals appear in the Node dock and are connectable from GDScript.
- [ ] Freed listeners don't receive events (no ObjectDisposedException).

## Checked
Godot docs (stable) pages and godotengine/godot master doc/classes XML fetched 2026-10-28.
Confirmed: C# signals page (`EventHandler` suffix, `SignalName`, `+=` events, `Connect` with `ConnectFlags`, automatic disconnect notes) and C# exports page (`ExportCategory`, `ExportGroup`, `ExportSubgroup`, `Godot.Collections`).
Removed: the same-file-name rule and the build-before-new-members note (not on the fetched pages).
Method: documentation only; no commands were run.
