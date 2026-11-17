---
id: computing-software.game-programming.gameplay-programming.strategy-pattern-for-weapons-and-ai
name: strategy-pattern-for-weapons-and-ai
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, game-programming-patterns, strategy-pattern, pluggable-behaviour, composition-over-inheritance, game-programming]
level: practitioner
status: draft
description: "Apply the Strategy pattern to swappable behaviours (fire modes, AI targeting) via interfaces or data assets, and know when a function or enum is better."
sources: ["https://refactoring.guru/design-patterns/strategy", "https://gameprogrammingpatterns.com/component.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Strategy pattern for weapons and AI

**Goal:** vary one behaviour (how a weapon fires, how an AI picks targets) independently of the object
that uses it, and swap it at runtime or per asset.

## Shape
```csharp
public interface IFireMode { void Fire(WeaponContext ctx); }
public sealed class SingleShot : IFireMode { public void Fire(WeaponContext c) => c.SpawnProjectile(c.Muzzle.forward); }
public sealed class Spread : IFireMode {
    public int pellets = 8; public float angle = 10f;
    public void Fire(WeaponContext c) { for (int i = 0; i < pellets; i++) c.SpawnProjectile(Jitter(c.Muzzle.forward, angle)); }
}
public class Weapon : MonoBehaviour {
    [SerializeReference] IFireMode fireMode = new SingleShot();   // pick concrete type in inspector
    public void Trigger() => fireMode.Fire(ctx);
    public void SetMode(IFireMode m) => fireMode = m;              // runtime swap (alt-fire, upgrades)
}
```
Engine-friendly variants: strategy as ScriptableObject/Data Asset/Resource (designer-selectable, shared
and stateless), Unreal `UObject` instanced subobjects (`UPROPERTY(EditAnywhere, Instanced)`).

## Context object
Pass what strategies need (`WeaponContext` with muzzle, owner, ammo, spawn functions) rather than the
whole weapon — keeps strategies testable and prevents them reaching into everything.

## Stateless vs stateful
- Stateless strategies can be shared (one asset used by 100 weapons).
- Stateful ones (burst counter, charge time) must be per-instance — instantiate/clone them, or keep state
  in the context.

## When not to
- Two or three fixed variants that never change at runtime: an enum + switch is clearer.
- Single method with no data: a delegate/function reference (`Func<Target[], Target>`) is a strategy
  without the class ceremony.
- Variation across many axes at once -> components or data-driven composition rather than strategies for
  everything.

## Gotchas
- Shared mutable strategy assets leak state between users (classic ScriptableObject bug).
- Serializing interface fields needs engine support (`[SerializeReference]` in Unity, instanced UObjects in
  Unreal, Resources in Godot).

## Verify
- [ ] Unit test each strategy with a fake context.
- [ ] Switching fire mode at runtime doesn't reset unrelated weapon state.
