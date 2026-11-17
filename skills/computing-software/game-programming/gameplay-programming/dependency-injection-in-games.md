---
id: computing-software.game-programming.gameplay-programming.dependency-injection-in-games
name: dependency-injection-in-games
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, di-container, dependency-injection, service-locator, game-programming]
level: practitioner
status: draft
description: "Use dependency injection in games: constructor injection, composition roots, scoped containers (Zenject, VContainer) and when a service locator is simpler."
sources: ["https://vcontainer.hadashikick.jp/", "https://gameprogrammingpatterns.com/service-locator.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dependency injection containers in games

**Goal:** wire systems together without singletons, so systems are swappable and testable.

## Plain DI first
Constructor injection with a hand-written **composition root** (one place that builds everything at
boot) is DI without a container and is often enough:
```csharp
var audio = new FmodAudio(); var save = new SteamSave();
var game  = new GameSession(audio, save, new Analytics(httpClient));
```

## Containers (Unity examples)
- **VContainer** (fast, source-generated) and **Zenject/Extenject**: register in a LifetimeScope,
  resolve into MonoBehaviours.
```csharp
public class GameLifetimeScope : LifetimeScope {
    protected override void Configure(IContainerBuilder b) {
        b.Register<IAudio, FmodAudio>(Lifetime.Singleton);
        b.Register<EnemySpawner>(Lifetime.Scoped);
        b.RegisterComponentInHierarchy<HudView>();
        b.RegisterEntryPoint<GameLoop>();              // ITickable etc.
    }
}
```
- **Scopes** match game lifetimes: project (app), scene, and per-match child scopes, disposed when
  the match ends, which cleans up subscriptions.

## Trade-offs
- Reflection-based containers cost startup time and allocate; on IL2CPP use code-gen or pre-baking.
- Overuse hides the object graph; if everything is injected everywhere, nobody knows what depends
  on what. Inject only cross-cutting services and system collaborators, not data.
- A service locator (Nystrom) is simpler for small games and engines; DI wins when you need test
  doubles and multiple lifetimes.

## Pitfalls
- Resolving from the container inside gameplay code (`container.Resolve<T>()` everywhere) is a
  service locator with extra steps.
- Circular dependencies show up at resolve time; break them with events.

## Verify
- Construct a system in a unit test with fakes, no scene loaded.
