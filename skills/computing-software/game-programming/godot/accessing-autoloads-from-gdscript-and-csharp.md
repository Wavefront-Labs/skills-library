---
id: computing-software.game-programming.godot.accessing-autoloads-from-gdscript-and-csharp
name: accessing-autoloads-from-gdscript-and-csharp
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, autoload-access, autoload, csharp, singletons, game-programming]
level: practitioner
status: docs-checked
description: "Access Godot autoloads safely from GDScript and C#: global names, /root paths, typed references, static Instance patterns and access from tool scripts and threads."
sources: ["https://docs.godotengine.org/en/stable/tutorials/scripting/singletons_autoload.html", "https://docs.godotengine.org/en/stable/tutorials/scripting/cross_language_scripting.html", "https://docs.godotengine.org/en/stable/tutorials/performance/thread_safe_apis.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Accessing autoloads from GDScript and C#

**Goal:** typed, null-safe access to global services in both languages.

## GDScript
With the **Enable** column checked in the Autoload list (the default), the singleton can be accessed
directly by its name in GDScript:
```gdscript
GameState.score += 10           # typed: autocompletion and static checks work
Events.player_died.emit()
```
Autoloads are ordinary nodes under the root, so `get_node("/root/GameState")` also works and returns
`Node`; cast it to the script type if you need typed access.

## C#
The **Enable** column has no effect in C# code. Options:
```csharp
// 1. Path lookup (cache it)
var gs = GetNode<GameState>("/root/GameState");

// 2. Static Instance set by the autoload itself (common)
public partial class GameState : Node {
    public static GameState Instance { get; private set; }
    public override void _Ready() => Instance = this;
    public override void _ExitTree() { if (Instance == this) Instance = null; }
}
// usage
GameState.Instance.Score += 10;
```
The autoload tutorial assigns `Instance` in `_Ready()`. Autoloads are added to the tree top to bottom
before the main scene, so keep an autoload above the ones that use it.

## Cross-language
A GDScript autoload used from C#: `GetNode("/root/Settings").Call("set_volume", 0.5)` or `.Get("volume")`.
C# members are accessed from GDScript by their C# names (for example `MyProperty`), as the
cross-language documentation shows.

## Where access is valid
- In `_init` of other nodes the tree may not be ready; access in `_ready` or later.
- From threads: interacting with the active scene tree is not thread-safe; defer such calls to the main
  thread with `call_deferred`.

## Gotchas
- Static `Instance` hides lifetime; reset it in `_ExitTree` so tests and scene reloads do not hold stale
  references.
- Never remove an autoload with `free()` or `queue_free()` at runtime; the engine crashes.

## Verify
- [ ] No hard-coded `/root/...` strings scattered in code; one access pattern per language.

## Checked

2026-10-25, against godot-docs master ("latest" docs, last commit 2026-10-24). Confirmed in the autoloads tutorial: the Enable column, direct GDScript access, C# static Instance assigned in _Ready(), access via get_node on the root, the free()/queue_free() crash warning; in the cross-language page: GodotObject.Get() and Call() from C#, and C# members used by name from GDScript; in the thread-safe APIs page: scene tree access needs call_deferred. Unconfirmed remarks about tool scripts, _EnterTree timing and storing autoload references in Resources were removed.

Method: documentation only; no commands were run.
