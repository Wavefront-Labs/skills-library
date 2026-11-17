---
id: computing-software.game-programming.unity.unity-test-mocking-with-nsubstitute
name: unity-test-mocking-with-nsubstitute
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-test-framework, nsubstitute, test-doubles, mocking, game-programming]
level: practitioner
status: draft
description: "Mock dependencies in Unity tests with NSubstitute (or hand-written fakes): installing the DLL, interface seams, Received checks, and what you cannot mock in Unity."
sources: ["https://nsubstitute.github.io/help/getting-started/", "https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/index.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mocking with NSubstitute in Unity tests

**Goal:** unit-test gameplay logic in isolation from input, time, saves, network and other systems.

## Install
NSubstitute is not a Unity package: add `NSubstitute.dll` and its dependency
`Castle.Core.dll` (plus `System.Threading.Tasks.Extensions` / `System.Runtime.CompilerServices.Unsafe`
depending on version) to a `Plugins/Testing` folder, set the plugin import to **Editor only** (or
include only in the test asmdef via "Override References" + "Assembly References"). Some teams use a
NuGet-for-Unity package instead.

## Seams
Mocks need interfaces or virtual members. Put logic in plain C# classes that take interfaces:
```csharp
public interface IClock { float Now { get; } }
public interface ISaveStore { void Write(string key, string json); }
public class Cooldown { readonly IClock clock; ... public bool Ready => clock.Now >= readyAt; }
```

## Test
```csharp
[Test]
public void Ready_after_duration() {
    var clock = Substitute.For<IClock>();
    clock.Now.Returns(0f);
    var cd = new Cooldown(clock, duration: 2f); cd.Trigger();
    clock.Now.Returns(2.01f);
    Assert.IsTrue(cd.Ready);
}
[Test]
public void Saves_on_checkpoint() {
    var store = Substitute.For<ISaveStore>();
    new CheckpointService(store).Reach("cp1");
    store.Received(1).Write("checkpoint", Arg.Is<string>(s => s.Contains("cp1")));
}
```

## What you cannot mock
`MonoBehaviour`, `Transform`, `Time`, `Physics`, `Input` statics and sealed engine types. Wrap them
behind interfaces (thin adapter MonoBehaviour) or use Play Mode tests with real objects.

## Gotchas
- IL2CPP/AOT: Castle DynamicProxy needs runtime codegen — run mocks in Edit Mode tests or Mono
  backend only; do not ship NSubstitute in player builds.
- Hand-written fakes are often simpler and faster than mocks for data-like dependencies.
- Over-mocking couples tests to implementation; assert outcomes, use `Received` only for true side
  effects (saves, network sends).

## Verify
- [ ] Test asmdef references NSubstitute; runtime asmdefs do not.
- [ ] Tests run headless in CI in Edit Mode.
