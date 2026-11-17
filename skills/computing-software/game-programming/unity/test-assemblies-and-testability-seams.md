---
id: computing-software.game-programming.unity.test-assemblies-and-testability-seams
name: test-assemblies-and-testability-seams
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-testing, test-assembly, asmdef, testability, humble-object, dependency-injection, game-programming]
level: practitioner
status: draft
description: "Structure Unity code for testing: test assembly asmdefs, InternalsVisibleTo, humble-object MonoBehaviours, plain C# logic, and seams for time, input and randomness."
sources: ["https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/workflow-create-test-assembly.html", "https://docs.unity3d.com/Manual/ScriptCompilationAssemblyDefinitionFiles.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Test assemblies and testability seams

**Goal:** most game logic testable in fast Edit Mode tests, because it doesn't need a scene to run.

## Test assemblies
- Tests must live in an asmdef with **Test Assemblies** ticked (adds `UNITY_INCLUDE_TESTS` define
  constraint and references nunit/TestRunner). They are excluded from player builds.
- Your game code must also be in asmdefs; test assemblies can't reference Assembly-CSharp.
- Edit Mode test asmdef: Include Platforms = Editor only. Play Mode test asmdef: all platforms.
- Expose internals instead of making everything public:
```csharp
// Game.Core/AssemblyInfo.cs
[assembly: System.Runtime.CompilerServices.InternalsVisibleTo("Game.Core.Tests")]
```

## Humble object
Keep MonoBehaviours thin: they read Unity state and forward to plain C# classes.
```csharp
public class Inventory {                                  // pure C#: Edit Mode testable
    readonly int capacity; readonly List<Item> items = new();
    public Inventory(int capacity) => this.capacity = capacity;
    public bool TryAdd(Item i) { if (items.Count >= capacity) return false; items.Add(i); return true; }
}

public class InventoryComponent : MonoBehaviour {         // humble: glue only
    [SerializeField] int capacity = 20;
    public Inventory Model { get; private set; }
    void Awake() => Model = new Inventory(capacity);
}

[Test] public void Add_WhenFull_Fails() {
    var inv = new Inventory(1); inv.TryAdd(new Item()); Assert.IsFalse(inv.TryAdd(new Item()));
}
```

## Seams for non-determinism
- **Time**: inject `Func<float> now` or an `IClock`; don't read `Time.time` inside logic classes.
- **Randomness**: pass a `System.Random` (or `Unity.Mathematics.Random`) with a seed.
- **Input**: logic consumes a `Vector2 move` / commands, not `Keyboard.current`. For Play Mode input
  tests, the Input System's `InputTestFixture` creates virtual devices (`Press(gamepad.buttonSouth)`).
- **Unity services/singletons**: interface + constructor parameter; a fake in tests.
- ScriptableObjects: `ScriptableObject.CreateInstance<T>()` in tests; destroy in teardown.

## Gotchas
- Static state survives between tests; reset or avoid it.
- Don't test Unity itself (that Rigidbody falls); test your rules.
- `[TestCase]` / `[TestCaseSource]` keep table-driven tests short.

## Verify
- [ ] Core logic tests run in Edit Mode in seconds without loading scenes.
- [ ] Player builds contain no test assemblies.
