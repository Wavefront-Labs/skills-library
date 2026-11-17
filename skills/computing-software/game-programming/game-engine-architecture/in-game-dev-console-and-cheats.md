---
id: computing-software.game-programming.game-engine-architecture.in-game-dev-console-and-cheats
name: in-game-dev-console-and-cheats
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, dev-console, cheat-commands, debug-commands, command-registry, autocomplete, game-programming]
level: practitioner
status: draft
description: "Build an in-game developer console: command registry with typed args, autocomplete and history, cvar integration, cheat gating, scripted exec files and stripping from shipping."
sources: ["https://developer.valvesoftware.com/wiki/Developer_Console_Control", "https://dev.epicgames.com/documentation/en-us/unreal-engine/console-commands-for-unreal-engine", "https://github.com/ocornut/imgui/blob/master/imgui_demo.cpp"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# In-game dev console and cheats

**Goal:** testers and developers can teleport, spawn, toggle debug draws, set cvars and run test
scripts in any build except shipping, without menus for each feature (Gregory ch. 10).

## Command registry
```cpp
using CmdFn = std::function<void(std::span<const std::string_view> args)>;
struct Command { const char* name; const char* help; CmdFn fn; uint32_t flags; };
void registerCommand(Command c);       // name-sorted map: supports prefix autocomplete

static AutoCommand cmdTeleport("teleport", "teleport <x> <y> <z>", [](auto args) {
    if (args.size() != 3) return log("usage: teleport <x> <y> <z>");
    player().setPosition({parseF(args[0]), parseF(args[1]), parseF(args[2])});
}, CMD_Cheat);
```
- Tokenise with quotes (`spawn "Big Troll" 3`), `;` to chain, and parse args with clear usage errors.
- Commands and cvars share one namespace and one autocomplete (Tab completes names, then enum values
  or asset names).
- History (up/down arrows) persisted to a file; `exec file.cfg` runs scripted command lists (test
  setups, benchmark sequences); `bind key "command"` for repeated actions.

## Execution safety
- Run commands on the game thread at a safe point in the frame (queue input from the console UI).
- Network games: commands execute on the right side. Client cheats must be **server RPCs validated
  by the server**, and only when the server allows cheats; Unreal `UCheatManager` exists only when
  cheats are enabled (`EnableCheats` / dev builds); Source `sv_cheats 1` gates `FCVAR_CHEAT`.
- Log every executed command with timestamp: bug reports then include how state was reached.

## UI
Toggle with backtick/tilde (and a controller chord or touch gesture on consoles/mobile). Show the
output log with filters by category and severity; Dear ImGui makes a full console in ~200 lines
(the ImGui demo contains an example console).

## Shipping
Compile the console and cheat commands out of shipping builds (`#if !SHIPPING`), not just hide the
key. Leftover cheat paths are a classic exploit and certification failure. Keep a curated, safe
subset if you ship a user-facing console (PC modding).

## Useful default commands
`help`, `find <text>`, `teleport`, `god`, `noclip`, `give <item> [n]`, `spawn <type> [n]`,
`timescale <x>`, `slomo`, `pause_ai`, `show <debugcategory>`, `stat <group>`, `screenshot`,
`quest.*`, `save/load <slot>`, `map <name>`, `exec <file>`.

## Verify
- [ ] Unknown command and wrong-argument cases print usage, never crash.
- [ ] Shipping build symbol/strings check finds no console command names.
- [ ] A client cannot run a cheat on a server with cheats disabled.
