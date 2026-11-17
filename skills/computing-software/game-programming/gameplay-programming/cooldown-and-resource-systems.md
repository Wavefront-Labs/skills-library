---
id: computing-software.game-programming.gameplay-programming.cooldown-and-resource-systems
name: cooldown-and-resource-systems
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, combat, cooldown-system, ability-cooldowns, charges, mana-stamina, resource-regeneration, game-programming]
level: practitioner
status: draft
description: "Build ability cooldowns and resources: timestamp-based cooldowns, charges with recharge, global cooldown, cooldown reduction, stamina/mana regen delay and UI-friendly queries."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/gameplay-ability-system-for-unreal-engine", "https://gameprogrammingpatterns.com/update-method.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cooldown and resource systems

## Store end times, not countdowns
```csharp
class Cooldown {
    double readyAt;                                      // game-time seconds
    public bool Ready(double now) => now >= readyAt;
    public void Start(double now, float duration) => readyAt = now + duration;
    public float Remaining(double now) => (float)System.Math.Max(0, readyAt - now);
    public float Fraction(double now, float duration) => duration <= 0 ? 0 : Remaining(now) / duration;
}
```
Timestamps need no per-frame update, survive pausing if you use a game clock that stops when paused,
serialize trivially, and are easy to replicate (send `readyAt` once). Use a double or integer ticks:
a float game clock loses precision after hours.

## Charges
```csharp
int charges = max; double nextChargeAt;
bool TryUse(double now) {
    Refill(now);
    if (charges == 0) return false;
    if (charges == max) nextChargeAt = now + rechargeTime;   // start recharging on first use
    charges--; return true;
}
void Refill(double now) {
    while (charges < max && now >= nextChargeAt) { charges++; nextChargeAt += rechargeTime; }
}
```

## Common rules
- **Global cooldown (GCD):** a shared short cooldown all abilities check, separate from their own.
- **Cooldown reduction:** apply when starting (`duration * (1 - cdr)`), clamp CDR (e.g. 40%) so
  abilities can't become spammable. Decide whether CDR changes affect running cooldowns.
- **Input buffering:** if pressed within ~0.1-0.2 s before ready, queue the cast so it fires on ready.
- **Resources (mana/stamina):** `current = min(max, current + regenRate * dt)` only after
  `now >= lastSpendTime + regenDelay`; deny actions when insufficient, or allow "exhausted" state
  for stamina (sprint stops, short lockout).
- Cost check and spend happen atomically in one function (`TryActivate`) to avoid double spend.

## Networking
Server owns cooldown truth; client predicts the start locally for responsive UI and corrects on
rejection. In Unreal GAS, cooldowns are GameplayEffects granting a cooldown tag; query with
`GetCooldownTimeRemainingAndDuration`.

## UI
Expose `Remaining` and `Fraction` for radial fills; show charges count; flash on ready.

## Verify
- [ ] Pause for 30 s: cooldowns don't progress if the design says paused time doesn't count.
- [ ] Charges recharge one at a time and keep the remainder correctly after multiple uses.
- [ ] Spam-press test never fires during cooldown or spends resources twice.
