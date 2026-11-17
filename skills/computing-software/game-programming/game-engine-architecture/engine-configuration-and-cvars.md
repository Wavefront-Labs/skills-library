---
id: computing-software.game-programming.game-engine-architecture.engine-configuration-and-cvars
name: engine-configuration-and-cvars
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, cvars, console-variables, engine-configuration, ini-config, command-line-args, game-programming]
level: practitioner
status: draft
description: "Design engine configuration and console variables: typed self-registering cvars, flags (cheat, read-only, saved), layered ini/command-line priority, change callbacks."
sources: ["https://www.gameenginebook.com/", "https://dev.epicgames.com/documentation/en-us/unreal-engine/console-variables-cplusplus-in-unreal-engine", "https://developer.valvesoftware.com/wiki/Developer_Console_Control"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Engine configuration and cvars

**Goal:** every tunable (render quality, physics substeps, debug toggles, network rates) is a named,
typed variable settable from config files, the command line and the in-game console, without
recompiling (Gregory ch. 6.6; id Tech / Source / Unreal cvar systems).

## Self-registering typed cvars
```cpp
template <class T> struct CVar {
    CVar(const char* name, T def, const char* help, uint32_t flags = 0);
    T get() const; void set(T v, CVarSource src);
    void onChange(std::function<void(T)> cb);
};
static CVar<int>   r_shadowQuality("r.ShadowQuality", 2, "0=off 1=low 2=med 3=high", CVF_Saved);
static CVar<float> net_tickRate("net.TickRate", 30.f, "server ticks per second", CVF_ReadOnlyAfterInit);
static CVar<bool>  g_godMode("g.GodMode", false, "invulnerable player", CVF_Cheat);
```
Static registration into a global registry is fine here because cvars are plain data (the registry
must use a function-local static to avoid init-order issues).

## Flags that matter
- **Cheat:** only settable when cheats are enabled (dev builds / `sv_cheats`); never in shipping
  multiplayer.
- **Read-only / init-only:** settable from config/command line, not at runtime.
- **Saved / archive:** persisted to the user config (graphics settings).
- **Replicated / server-authoritative:** server value pushed to clients (`FCVAR_REPLICATED` in Source).
- **Render-thread safe:** Unreal `ECVF_RenderThreadSafe` shadows the value for the render thread.

## Layered sources and priority
Lowest to highest: compiled default < engine ini < platform ini < project ini < device profile /
scalability group < user saved config < command line < console at runtime. Record **which source** set
the current value; when a user's setting "does not stick" it is always priority. Unreal tracks
`ECVF_SetByConstructor ... ECVF_SetByConsole` and ignores lower-priority sets with a log warning.

## Change callbacks
Apply changes via callbacks (recreate shadow maps when quality changes) on a safe point (start of
frame), not inside the console command handler on whatever thread typed it.

## Unreal specifics
`static TAutoConsoleVariable<int32> CVarFoo(TEXT("r.Foo"), 1, TEXT("help"), ECVF_Scalability);`;
read with `CVarFoo.GetValueOnGameThread()`; set in `DefaultEngine.ini` `[SystemSettings]` or
`[ConsoleVariables]`, or `-ini:Engine:[SystemSettings]:r.Foo=0`, or `ExecCmds="r.Foo 0"`.

## Verify
- [ ] `help <name>` / `cvarlist` prints type, value, default, flags and the source that set it.
- [ ] Cheat cvars are rejected in a shipping build test.
- [ ] Changing a render cvar at runtime applies at the next frame without a crash.
