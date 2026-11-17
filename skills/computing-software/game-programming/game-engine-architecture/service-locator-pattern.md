---
id: computing-software.game-programming.game-engine-architecture.service-locator-pattern
name: service-locator-pattern
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, game-programming-patterns, service-locator, null-object, decorator-logging, dependency-injection, decoupling, game-programming]
level: practitioner
status: draft
description: "Implement a Service Locator for engine services: null-service default, logging decorators, scoping, and when DI or passing references wins."
sources: ["https://gameprogrammingpatterns.com/service-locator.html", "https://dev.epicgames.com/documentation/en-us/unreal-engine/programming-subsystems-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Service Locator pattern

**Goal:** global access to a service (audio, logging, analytics, save system) without coupling
callers to the concrete class or to who created it (Nystrom, GPP "Service Locator").

## Shape
```cpp
class Audio {
public:
    virtual ~Audio() = default;
    virtual void playSound(SoundId id) = 0;
    virtual void stopAllSounds() = 0;
};
class NullAudio : public Audio {            // null object: safe default, does nothing
public:
    void playSound(SoundId) override {}
    void stopAllSounds() override {}
};
class Locator {
public:
    static Audio& audio() { return *service_; }
    static void provide(Audio* s) { service_ = s ? s : &nullService_; }
private:
    static inline NullAudio nullService_;
    static inline Audio* service_ = &nullService_;
};
// startup: Locator::provide(new XAudio2Audio()); callers: Locator::audio().playSound(SFX_JUMP);
```
The null service means callers never null-check and the game runs headless (tests, servers, audio
device missing).

## Decorators
Wrap a service to add behaviour without touching callers:
`Locator::provide(new LoggedAudio(Locator::audio()))` logs every sound in a debug build. Same for
analytics (batching wrapper), file system (timing/tracing wrapper).

## Design decisions
- **When is it bound:** compile time (`#if`), configuration (data), or runtime (`provide`). Runtime
  binding allows swapping (mute audio for a cutscene, mock for tests).
- **Scope:** global for genuinely global services (logging, platform); per-world/per-level locators
  for things that differ between worlds (physics scene, AI manager) to avoid cross-world bugs in
  editors that host several worlds.
- **Missing service policy:** null object (most services), assert (services that must exist), or
  lazy creation.

## When not to use it
It is still a global: dependencies are hidden in call sites. Prefer passing references or
constructor injection where the dependency graph is small; use the locator for cross-cutting
services touched from many places. Engine equivalents: Unreal subsystems
(`GetGameInstance()->GetSubsystem<USaveSubsystem>()`) are scoped service locators; Unity projects use
a static `Services` registry or DI frameworks (VContainer, Zenject).

## Verify
- [ ] The game boots and plays with every optional service replaced by its null version.
- [ ] Unit tests provide mock services and restore defaults after each test.
- [ ] No caller includes a concrete service header.
