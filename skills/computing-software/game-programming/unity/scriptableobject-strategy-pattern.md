---
id: computing-software.game-programming.unity.scriptableobject-strategy-pattern
name: scriptableobject-strategy-pattern
category: computing-software
field: game-programming
product: unity
tags: [unity, so-strategy, scriptableobject, strategy-pattern, data-driven, game-programming]
level: practitioner
status: draft
description: "Implement pluggable strategy ScriptableObjects in Unity: abstract SO behaviours (targeting, movement, abilities) swapped per asset in the Inspector without code changes."
sources: ["https://unity.com/how-to/architect-game-code-scriptable-objects", "https://docs.unity3d.com/Manual/class-ScriptableObject.html", "https://gameprogrammingpatterns.com/type-object.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ScriptableObject strategy pattern

**Goal:** designers pick an enemy's targeting or an ability's effect from a dropdown of assets.

## Shape
```csharp
public abstract class TargetingStrategy : ScriptableObject {
    public abstract Transform Pick(Transform self, IReadOnlyList<Transform> candidates);
}

[CreateAssetMenu(menuName = "AI/Targeting/Nearest")]
public class NearestTarget : TargetingStrategy {
    public override Transform Pick(Transform self, IReadOnlyList<Transform> c) {
        Transform best = null; float bestD = float.MaxValue;
        foreach (var t in c) { float d = (t.position - self.position).sqrMagnitude; if (d < bestD) { bestD = d; best = t; } }
        return best;
    }
}

[CreateAssetMenu(menuName = "AI/Targeting/Lowest Health")]
public class LowestHealthTarget : TargetingStrategy { /* ... */ }

public class Turret : MonoBehaviour {
    [SerializeField] TargetingStrategy targeting;   // drag NearestTarget.asset
    void Update() { var t = targeting.Pick(transform, Sensors.Visible); /* ... */ }
}
```
Each asset can carry parameters (range, weights), so `Nearest_Short.asset` and `Nearest_Long.asset`
are two configurations of one class.

## Rules
- Strategies must be **stateless**: one asset is shared by every turret. Per-user state goes on the
  MonoBehaviour or in a context object passed in. Writing to SO fields at runtime leaks between users
  and, in the editor, persists after play mode.
- If a strategy truly needs per-instance state, give it a factory method returning a plain C# runtime
  object (`CreateRuntime()`), or `Instantiate(strategy)` once per user.
- Prefer `[SerializeReference]` with plain C# classes when the strategy is only ever owned by one
  object and needs no asset reuse.

## Gotchas
- Abstract SO fields show any subclass asset; filter with a custom attribute or keep folders tidy.
- Renaming a strategy class breaks asset script references unless you keep the file/class name or use
  `[MovedFrom]` for SerializeReference types.

## Verify
- [ ] Swapping the asset changes behaviour in play mode with no code change.
- [ ] Two users of one strategy asset never influence each other.
