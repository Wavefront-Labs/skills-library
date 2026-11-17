---
id: computing-software.game-programming.godot.cross-language-scripting-gdscript-csharp
name: cross-language-scripting-gdscript-csharp
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, gdscript, csharp, cross-language, interop, game-programming]
level: practitioner
status: docs-checked
description: "Call between GDScript and C# in one Godot project: instancing scripts across languages, Call/Get/Set by name, signals across the boundary, and the no-inheritance rule."
sources: ["https://docs.godotengine.org/en/stable/tutorials/scripting/cross_language_scripting.html", "https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/c_sharp_differences.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cross-language scripting GDScript to C#

**Goal:** mix C# for heavy systems and GDScript for glue without fragile interop.

## GDScript -> C#
```gdscript
var MyCSharpScript = load("res://Path/To/MyCSharpNode.cs")
var my_csharp_node = MyCSharpScript.new()      # instantiates the C# script
```
C# members are used with their C# (PascalCase) names from GDScript; calls are dynamic because C# classes are not
GDScript types.

## C# -> GDScript
C# is statically typed, so access GDScript through `GodotObject` methods:
```csharp
var myGDScript = GD.Load<GDScript>("res://path/to/my_gd_script.gd");
var myGDScriptNode = (GodotObject)myGDScript.New();
GD.Print(myGDScriptNode.Get("my_property"));
myGDScriptNode.Set("my_property", "value");
myGDScriptNode.Call("print_n_times", "Hello there!", 2);
```
`Get`, `Set` and `Call` take the GDScript member name (snake_case) as the first argument; `Call` passes the
remaining arguments to the method.

## Signals
- Connecting to a C# signal from GDScript is the same as connecting to a GDScript signal. C# signals are
  declared with `[Signal] public delegate void MySignalEventHandler();`.
- Connecting to a GDScript signal from C# only works with `Connect`, because no C# static types exist for
  GDScript-defined signals: `node.Connect("my_signal", Callable.From(MySignalHandler));` (use
  `Callable.From<string, int>(...)` for arguments).

## Limits
- A GDScript file cannot inherit from a C# script, and a C# script cannot inherit from a GDScript file; the docs say
  this is unlikely to change.
- In C#, Godot APIs use PascalCase and properties instead of getter/setter methods (`x.Name = "Friend"` rather than
  `set_name`); see "C# differences" for the utility function and constant mappings.
- Keep the cross-language surface small and coarse, and measure it with the profiler if it is called every frame.

## Verify
- [ ] Interop surface is a few coarse calls per frame at most.
- [ ] Renaming a C# or GDScript member breaks visibly (tests or startup checks), not silently at runtime.

## Checked
2026-10-28. Confirmed on the cross-language scripting and C# differences pages: load and `.new()` of C# scripts,
`GD.Load<GDScript>`, `Get`/`Set`/`Call`, `Connect` with `Callable.From`, `[Signal]` delegate naming, no cross-language
inheritance, PascalCase and properties. Removed (not on the pages): GDScript-to-C# callability rules for generic
methods, `.As<T>` conversion examples, signal-name suffix rule for GDScript connects, packed-array batching and
Variant marshalling cost claims, .NET editor requirement and the "C# not supported on web as of 4.4" statement.
Method: documentation only; no commands were run.
