---
id: computing-software.game-programming.multiplayer-networking.rollback-state-save-restore-and-synctest
name: rollback-state-save-restore-and-synctest
category: computing-software
field: game-programming
product: multiplayer-networking
tags: [multiplayer-networking, rollback-netcode, state-rollback, synctest, ggpo, save-state, determinism, game-programming]
level: advanced
status: draft
description: "Make game state cheap to save and restore for rollback netcode, and prove determinism with GGPO-style SyncTest: state layout, checksums, frame budgets and desync hunting."
sources: ["https://github.com/pond3r/ggpo/blob/master/doc/DeveloperGuide.md", "https://www.ggpo.net/", "https://github.com/johanhelsing/bevy_ggrs", "https://gafferongames.com/post/deterministic_lockstep/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fast state save/restore for rollback, and SyncTest

Rollback re-simulates up to ~8 frames whenever late remote input arrives, so **save + load + N
simulation steps must fit in one frame**.

## Make state snapshot-friendly
- All simulation state in **plain data**: fixed-size arrays/structs, indices instead of pointers,
  no heap objects owned by gameplay. Then save = `memcpy` into a ring buffer slot per frame.
- Separate simulation state (positions, velocities, health, RNG seed, timers, frame number) from
  presentation (particles, audio, animation blending, UI). Only simulation is saved.
- Engine objects (scene nodes, physics engines) are hard to snapshot; either keep the sim outside
  them (custom deterministic physics) or use a physics library with cheap world snapshots
  (e.g. Rapier, whose world state can be serialised and cloned).
- Ring buffer of `maxRollback + 2` saved states, indexed by `frame % size`.

```c
typedef struct { int frame; uint32_t rng; Player p[2]; Projectile shots[64]; int shotCount; } GameState;
GameState ring[MAX_ROLLBACK + 2];
void save(int f)  { ring[f % RING] = state; }
void load(int f)  { state = ring[f % RING]; }
uint32_t checksum(const GameState* s) { return fletcher32(s, sizeof *s); }   // padding must be zeroed
```

## GGPO callbacks
`save_game_state(buffer, len, checksum, frame)`, `load_game_state(buffer, len)`,
`advance_frame()` (simulate one frame with inputs from `ggpo_synchronize_input`), `free_buffer`.
GGRS/bevy_ggrs (Rust) use the same model with `SaveGameState`/`LoadGameState`/`AdvanceFrame` requests.

## SyncTest
`ggpo_start_synctest(&session, &cb, "game", players, inputSize, checkDistance)` runs single-player:
every frame it rolls back `checkDistance` frames and re-simulates, comparing checksums with the first
run. A mismatch means save/load or simulation is non-deterministic. Run it in CI with recorded input.

Typical desync causes it finds:
- State not saved (a static/global counter, a cached value, an RNG outside the state).
- Iterating unordered containers (hash maps, physics contact order).
- Uninitialised struct padding in the checksummed bytes.
- Floating-point differences from compiler flags/SIMD paths (cross-platform: use fixed point).
- Presentation code feeding back into simulation (animation events changing state).

## Rollback side effects
Sounds and VFX triggered during re-simulation must be deduplicated: key them by (frame, entity,
event) and only play when first confirmed, or cancel ones that a rollback removed.

## Verify
- [ ] SyncTest with check distance 7 passes for a 10-minute recorded match.
- [ ] Profile worst case: load + 8 advances + save stays under ~50% of the frame budget.
