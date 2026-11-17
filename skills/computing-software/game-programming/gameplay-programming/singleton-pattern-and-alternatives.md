---
id: computing-software.game-programming.gameplay-programming.singleton-pattern-and-alternatives
name: singleton-pattern-and-alternatives
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, game-programming-patterns, singleton-pattern, global-state, dependency-injection, static-classes, testability, game-programming]
level: practitioner
status: draft
description: "Decide when a singleton is acceptable in game code and what to use instead: passing references, base-class access, existing globals, service locators, and lifetime/order pitfalls."
sources: ["https://gameprogrammingpatterns.com/singleton.html", "https://gameprogrammingpatterns.com/service-locator.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Singleton pattern and alternatives

**Goal:** avoid the global-state mess singletons create while still giving systems easy access to
the services they need (Nystrom, GPP "Singleton": "use it sparingly").

## What a singleton gives (and costs)
Gives: one instance, global access, lazy creation. Costs:
- Hidden dependencies: any code can reach any manager; coupling grows silently.
- Initialisation order bugs (manager A's constructor uses manager B before B exists).
- Hard to test (cannot substitute a fake) and to reset (Unity domain-reload-off, new game sessions).
- Concurrency: lazy initialisation races in multithreaded engines.
- Often the class does not need to be a single instance at all (two audio listeners in split-screen,
  multiple worlds in PIE).

## Prefer, in order
1. **Pass it in**: functions/constructors receive what they use (`render(Context&)`, `ai.update(world)`).
   Most "everyone needs it" cases are really "a few systems need it".
2. **Get it from a base class**: `GameObject` provides protected `log()`, `audio()` accessors
   (Nystrom's Subclass Sandbox idea) so only subclasses reach it.
3. **Piggyback an existing global**: one `Game`/`World` object owns Audio, Physics, Save; access
   `game.audio()`. One global instead of ten.
4. **Service locator**: interface + registry with a null service default; swap implementations
   (logging audio in debug, silent audio in tests), per Nystrom's Service Locator chapter.
5. **Engine-managed lifetimes**: Unreal subsystems, Godot autoloads, Unity bootstrap prefab with
   explicit references.

## If you still use one
- Create eagerly in a known startup order (explicit `init()`/`shutdown()` called by the engine core),
  not lazily on first access.
- Keep it stateless or resettable (`reset()` on new game; statics reset for editor play sessions).
- Expose an interface, not the concrete class, so tests can replace it.
- Never let a singleton hold references to scene objects that may be destroyed.

## Smell checklist
`Manager` suffix classes multiplying, `XManager.Instance.Y.Z` chains, tests that need the full game
running, bugs only in the second play session: all point to singleton overuse.

## Verify
- [ ] Each remaining global has documented owner, init order and reset behaviour.
- [ ] Core gameplay logic unit-testable with fakes (no singleton access inside).
- [ ] Starting a second game session without restarting the app behaves like the first.
