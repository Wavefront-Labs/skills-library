---
id: computing-software.game-programming.gameplay-programming.live-tuning-and-data-hot-reload
name: live-tuning-and-data-hot-reload
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, data-driven-design, live-tuning, hot-reload-data, tuning-variables, game-programming]
level: practitioner
status: draft
description: "Tune gameplay live: exposing tunables, hot-reloading data files while playing, debug menus and cvars, applying changes safely mid-session, and saving tuned values back."
sources: ["https://docs.unity3d.com/Manual/class-ScriptableObject.html", "https://dev.epicgames.com/documentation/en-us/unreal-engine/console-variables-cplusplus-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Live tuning and data hot-reload

**Goal:** designers change jump height, enemy HP or spawn rates while the game runs and see the result
immediately, then keep the values.

## Expose tunables
- Data assets/files (ScriptableObjects, Unreal Data Assets/DataTables, Godot Resources, JSON) instead of
  constants in code.
- Read tunables at use time (or subscribe to change events) — values cached at spawn won't reflect
  edits.
- Console variables for quick numeric tweaks (`cvar player.jumpHeight 3.2`); Unreal
  `TAutoConsoleVariable` with `ECVF_Cheat`, custom cvar systems elsewhere.

## Hot reload
- Engine editors already reload assets in play mode (Unity SO edits apply live; Unreal PIE uses asset
  edits; Godot resources reload on save).
- Builds on devices: file watcher (dev builds) on loose data files or a network channel from a tuning
  tool pushes new values:
```
watcher.Changed += path => {
    var data = Parse(File.ReadAllText(path));
    if (Validate(data, out var errors)) { Tuning.Apply(data); Log("reloaded"); }
    else Log(errors);                       // keep old values on bad data
};
```
- Apply on the main thread at a safe point (start of frame).

## Applying safely
- Changes to per-instance derived values: either recompute on change (`OnTuningChanged` event) or only
  affect new spawns — document which.
- Structural changes (new enemy type) usually need a restart; numeric tweaks shouldn't.

## Debug menus
In-game tweak menu (Dear ImGui, engine debug UI) bound to tunable fields with sliders, reset-to-default,
and "save to asset" in the editor. Group by system; include search.

## Saving tuned values
- In editor: edits to assets are saved by the editor (Unity: SO changes at runtime persist — desired
  here, careful elsewhere).
- From device: export changed values as a patch file/diff to commit.

## Gotchas
- Live-tuned values diverging between multiplayer peers -> desyncs; only allow on server or sync them.
- Tuning frame-rate dependent values (per-frame accelerations) misleads; units per second.
- Leaving cheats/tuning channels in shipping builds; strip with defines.

## Verify
- [ ] Change jump height file on a dev build: next jump uses it without restart.
- [ ] Invalid data reload logs errors and keeps previous values.
