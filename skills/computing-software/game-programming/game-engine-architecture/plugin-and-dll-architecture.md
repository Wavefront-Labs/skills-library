---
id: computing-software.game-programming.game-engine-architecture.plugin-and-dll-architecture
name: plugin-and-dll-architecture
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, plugin-architecture, dll, hot-reload, game-programming]
level: practitioner
status: draft
description: "Structure an engine as plugins: C ABI plugin interfaces, registries, DLL loading and hot reload of game code, ownership across module boundaries."
sources: ["https://ourmachinery.com/post/little-machines-working-together-part-1/", "https://learn.microsoft.com/en-us/windows/win32/dlls/dynamic-link-library-best-practices"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Plugin and DLL architecture

**Goal:** engine features and game code as separately built modules that load, unload and reload.

## Plugin interface
Use a C ABI for stability across compilers and versions:
```c
struct plugin_api { uint32_t version; void (*load)(struct registry* r, bool reload);
                    void (*unload)(struct registry* r, bool reload); };
// each DLL exports:
__declspec(dllexport) const struct plugin_api* get_plugin_api(void);
```
A **registry** maps interface names/versions to function tables; plugins register what they provide
and query what they need (Our Machinery's API registry design).

## Loading
- `LoadLibraryW`/`GetProcAddress` (Windows), `dlopen`/`dlsym` (POSIX).
- Resolve dependencies by querying the registry lazily, not at link time.

## Hot reload of game code
1. Copy the DLL (and PDB) to a temp name before loading so the compiler can overwrite the original
   (Windows locks loaded DLLs; also patch the PDB path or use unique PDB names per build).
2. On change: call `unload(reload=true)`, `FreeLibrary`, load the new copy, call `load(reload=true)`.
3. **State lives outside the DLL:** all persistent memory allocated by the host or in a state block
   passed in, so function pointers are re-fetched but data survives. Vtables and function pointers
   stored in data become invalid after reload; re-register callbacks on load.
Live++ and Unreal Live Coding patch functions in place as an alternative.

## Boundary rules
- Memory allocated in one module freed by the same allocator (pass the engine allocator in).
- No STL types across the C ABI (layout differs between builds).
- Static/global state is per DLL; singletons duplicate across modules.

## Verify
- Change a gameplay function, rebuild, and see behaviour change without restarting; repeat 100
  reloads without leaks.
