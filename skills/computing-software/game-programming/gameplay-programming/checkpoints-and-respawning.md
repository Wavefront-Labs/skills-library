---
id: computing-software.game-programming.gameplay-programming.checkpoints-and-respawning
name: checkpoints-and-respawning
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, game-state, checkpoint-system, respawn, level-state-reset, game-programming]
level: practitioner
status: draft
description: "Design checkpoints and respawn: what state to snapshot vs reset, checkpoint activation rules, respawn sequencing, persistent pickups and saving checkpoints to disk."
sources: ["https://gameprogrammingpatterns.com/command.html", "https://docs.godotengine.org/en/stable/tutorials/io/saving_games.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Checkpoints and respawning

**Goal:** dying returns the player to a fair point with the world in a consistent state — no duplicate
pickups, no stuck doors, no lost progress.

## Decide what persists across death
| Category | Typical rule |
|---|---|
| Player position/health | reset to checkpoint values |
| Collected keys / quest items | keep if collected before checkpoint; revert if after (design choice) |
| Consumables/currency | often kept (less frustration) |
| Enemies | respawn all, or only those since checkpoint |
| Doors/switches/puzzles | revert to checkpoint snapshot or reset room |
| One-shot events/cutscenes | keep "seen" flags |
Write this table per game; most respawn bugs are undecided rows.

## Implementation
- On checkpoint activation: snapshot **player state** and a set of **world flags** (switches, opened
  doors, collected ids) into a `CheckpointData`.
- Objects with resettable state implement an interface:
```csharp
interface IResettable { void Capture(CheckpointData d); void Restore(CheckpointData d); }
```
  Stable ids per object (scene GUID / authored id) key their saved state.
- On respawn: fade out -> restore world state -> despawn transient objects (projectiles, temporary
  enemies) -> respawn enemies per rule -> place player (with physics teleport reset) -> brief i-frames
  -> fade in -> give control.

## Activation rules
- Only activate checkpoints that are "safer" than the current one (progression order), to avoid
  backtracking resets.
- Don't activate while in combat, falling, or with a lethal hazard about to resolve.
- Feedback: visual/audio confirmation; optional heal.

## Saving to disk
Checkpoint data is the save file at that point in many games; write it asynchronously and atomically
when activated. Separate "continue" (last checkpoint) from manual save slots if both exist.

## Gotchas
- Respawning inside a collider or while enemies camp the checkpoint: offset spawn points, clear radius.
- Physics objects moved after checkpoint (crates) need Capture/Restore or room-reset rules.
- Timers and coroutines on world objects must be canceled on restore.

## Verify
- [ ] Die after collecting an item post-checkpoint: matches the persistence table.
- [ ] Death spam test (100 respawns) leaves object counts stable.
