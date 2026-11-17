---
id: computing-software.game-programming.game-engine-architecture.subsystem-startup-and-shutdown-order
name: subsystem-startup-and-shutdown-order
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, subsystem-startup, engine-initialization, static-initialization-order, shutdown-order, dependency-order, game-programming]
level: advanced
status: draft
description: "Start and stop engine subsystems in a defined order: explicit startUp/shutDown over static constructors, dependency ordering, reverse shutdown, Unreal module phases."
sources: ["https://www.gameenginebook.com/", "https://isocpp.org/wiki/faq/ctors#static-init-order", "https://dev.epicgames.com/documentation/en-us/unreal-engine/programming-subsystems-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Subsystem start-up and shut-down order

**Goal:** memory, file system, rendering, audio, physics and gameplay managers come up in dependency
order and go down in reverse, deterministically (Gregory, Game Engine Architecture ch. 6.1).

## Avoid static-constructor initialisation
Global singleton objects constructed before `main` run in an **unspecified order across translation
units** (the static initialisation order fiasco), and destructors run in reverse of that unknown
order. Meyers singletons (function-local statics) fix construction on first use but still give no
control over shutdown order.

## Explicit startUp/shutDown (Gregory's approach)
```cpp
class RenderManager {
public:
    RenderManager() {}           // do nothing
    ~RenderManager() {}          // do nothing
    void startUp();              // real init, may use other managers
    void shutDown();
};
MemoryManager gMemoryManager; FileSystemManager gFileSystemManager; /* ... */

int main() {
    gMemoryManager.startUp();
    gFileSystemManager.startUp();
    gConfig.startUp();           // needs file system
    gRenderManager.startUp();    // needs config, memory
    gAudioManager.startUp();
    gPhysicsManager.startUp();
    gGameManager.startUp();
    gGameManager.run();
    // shut down in exact reverse order
    gGameManager.shutDown(); gPhysicsManager.shutDown(); gAudioManager.shutDown();
    gRenderManager.shutDown(); gConfig.shutDown(); gFileSystemManager.shutDown(); gMemoryManager.shutDown();
}
```
The order is visible in one place and trivially reviewable. For many subsystems, register them with
declared dependencies and topologically sort; still shut down in reverse of the computed start order.

## Rules
- `startUp` returns success/failure; on failure, shut down the already-started ones in reverse and
  report which failed (driver missing, audio device absent: audio may degrade to a null device).
- Nothing does real work in constructors/destructors of global objects.
- Shutdown must tolerate partial init (e.g. crash during load), and must flush logs and saves before
  memory and file systems go down. Consider skipping full teardown in shipping (`_exit` after flush)
  for fast quit, but keep it in dev builds to catch leaks.
- Threads: stop job systems and streaming threads before the subsystems they touch.

## Engine mapping
- **Unreal:** modules load in phases (`LoadingPhase` in `.uplugin`/`.uproject`: `PostConfigInit`,
  `PreDefault`, `Default`, `PostEngineInit`); `StartupModule`/`ShutdownModule`. Subsystems
  (`UEngineSubsystem`, `UGameInstanceSubsystem`, `UWorldSubsystem`) get `Initialize`/`Deinitialize`
  tied to their outer's lifetime; use `Collection.InitializeDependency<UOther>()` for ordering.
- **Unity:** `[RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.SubsystemRegistration)]` etc.,
  or a bootstrap scene that initialises services in order.
- **Godot:** autoload order in Project Settings (top first).

## Verify
- [ ] Start-up order is printed in the log with timings per subsystem.
- [ ] Forcing each subsystem's startUp to fail exits cleanly with a clear message.
- [ ] Leak checker reports zero allocations after full shutdown in dev builds.
