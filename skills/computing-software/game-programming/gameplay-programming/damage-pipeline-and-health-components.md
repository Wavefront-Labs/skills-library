---
id: computing-software.game-programming.gameplay-programming.damage-pipeline-and-health-components
name: damage-pipeline-and-health-components
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, hitbox, combat-timing, damage-system, health-component, damage-types, resistances, invulnerability, death-handling, game-programming]
level: practitioner
status: draft
description: "Design a damage pipeline: typed damage events, modifier stages (armor, resistances, crits), a reusable health component, invulnerability and single-fire death."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/damage-in-unreal-engine", "https://gameprogrammingpatterns.com/component.html", "https://dev.epicgames.com/documentation/en-us/unreal-engine/gameplay-ability-system-for-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Damage pipeline and health components

**Goal:** one consistent path for all damage (bullets, fire, falls, explosions) that is easy to extend
with armor, resistances, crits and immunity, and never double-kills.

## Damage event
```
struct DamageEvent {
    float amount;
    DamageType type;          // Physical, Fire, Poison... (tag or enum)
    Entity instigator;        // who caused it (for kill credit, friendly fire)
    Entity source;            // what dealt it (projectile, trap)
    Vec3 hitPoint, hitNormal;
    Bone hitBone;             // headshot multipliers
    bool canCrit;
}
```

## Pipeline stages (ordered, data-driven)
```
1. Validate: target alive? friendly fire allowed? invulnerable (i-frames, spawn protection)?
2. Attacker modifiers: damage buffs, crit roll, weakpoint multiplier (bone)
3. Defender modifiers: armor (flat or % formula), resistances by type, shields absorb first
4. Clamp: min damage (e.g. 1), max per hit
5. Apply: health -= final; record last instigator
6. Notify: OnDamaged(event, final) -> UI numbers, hit reactions, sounds, AI perception
7. Death check: if health <= 0 and not dead: dead = true; OnDeath(event) exactly once
```
Armor formula example: `final = amount * 100 / (100 + armor)` (diminishing returns, never zero).
Keep each stage a small function or modifier object so designers can reorder/add.

## Health component
```csharp
public class Health : MonoBehaviour, IDamageable
{
    [SerializeField] float max = 100;
    public float Current { get; private set; }
    public bool IsDead { get; private set; }
    public event Action<DamageEvent, float> Damaged;
    public event Action<DamageEvent> Died;
    float invulnerableUntil;

    void Awake() => Current = max;
    public void ApplyDamage(DamageEvent e)
    {
        if (IsDead || Time.time < invulnerableUntil) return;
        float final = DamagePipeline.Resolve(e, this);
        Current = Mathf.Max(Current - final, 0);
        Damaged?.Invoke(e, final);
        if (Current <= 0) { IsDead = true; Died?.Invoke(e); }
    }
    public void Heal(float a) { if (!IsDead) Current = Mathf.Min(Current + a, max); }
    public void GrantInvulnerability(float seconds) => invulnerableUntil = Time.time + seconds;
}
```
Death consumers (ragdoll, loot, score, respawn) subscribe to `Died`; Health does not know about them.

## Engine equivalents
Unreal: `AActor::TakeDamage` / `UGameplayStatics::ApplyDamage` with `UDamageType`, or GAS (damage as
a Gameplay Effect with an execution calculation; attributes Health/Shield). Godot: a Health node with
signals.

## Pitfalls
- Multiple hits in one frame both pass the "alive" check before death processing: the `IsDead` flag set
  synchronously prevents double death.
- Damage over time should go through the same pipeline (each tick an event) so resistances apply.
- Multiplayer: only the server applies damage; clients receive replicated health.

## Verify
- [ ] Unit tests for the pipeline: armor, resistance, crit, min damage cases.
- [ ] Shotgun blast killing a target fires Died exactly once.
- [ ] Invulnerability windows block all damage types including DoT.
