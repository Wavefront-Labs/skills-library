---
id: computing-software.game-programming.gameplay-programming.quest-and-objective-systems
name: quest-and-objective-systems
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, quest-system, objectives, quest-graph, game-events, data-driven-design, save-data, game-programming]
level: practitioner
status: draft
description: "Implement a data-driven quest system: quest/stage/objective data, event-driven objective counters, prerequisites and branching, journal UI hooks, and save/version-safe progress."
sources: ["https://gameprogrammingpatterns.com/event-queue.html", "https://dev.epicgames.com/documentation/en-us/unreal-engine/gameplay-tags", "https://gameprogrammingpatterns.com/observer.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Quest and objective systems

**Goal:** designers author quests as data; gameplay code only emits events; progress survives saves
and patches.

## Data model
```
QuestDef     id, title, prerequisites [questId | flag], stages [StageDef], rewards
StageDef     id, objectives [ObjectiveDef], completion: all | any, next: stageId | branch rules
ObjectiveDef id, type (Kill, Collect, Reach, Talk, Interact, Custom), target (tag/id), count, optional
QuestState   questId, status (Locked/Available/Active/Completed/Failed), stageId, counters {objId: n}
```
Definitions are immutable assets (ScriptableObject, Data Asset, Godot Resource, JSON); state is a
small serialisable record. Never store progress on the definition asset.

## Event-driven progress
Gameplay emits domain events, never calls the quest system directly:
`GameEvents.Emit(Killed{enemyTag="Enemy.Wolf"})`, `ItemAcquired{id, count}`, `EnteredArea{id}`,
`DialogueNodeReached{id}`. The quest manager subscribes and, for each **active** objective whose type
and target match, increments its counter and checks stage completion.
- Index active objectives by event type to avoid scanning every quest per event.
- Match targets with tags/hierarchies (`Enemy.Wolf` satisfies `Enemy`), e.g. Unreal Gameplay Tags.
- "Collect" objectives should evaluate current inventory on activation too (player may already hold
  the items), and decrement if items are dropped when the design requires holding them.

## Branching and failure
Stage `next` can be a rule list: first rule whose condition holds (`flag:spared_bandit`) wins.
Fail conditions (timer, NPC died) are objectives of their own that move the quest to Failed.
World-state changes (spawn NPC, unlock door) are driven by stage enter/exit actions, so loading a
save re-applies them by replaying the current stage's enter actions.

## Save and patch safety
- Save quest **ids, stage ids, counters**, never indices; ids are permanent.
- On load, validate against current definitions: unknown stage -> fall back to the quest's
  migration map or nearest earlier stage; counters clamp to new counts.
- Patch adds an objective to a completed stage: completed stays completed.

## UI hooks
Raise `QuestUpdated(questId)` after each change; journal, HUD tracker and waypoint marker listen.
Throttle "objective updated" toasts for rapid counters (collect 50).

## Verify
- [ ] Each objective type completes from a pure event in an automated test, with no UI.
- [ ] Picking up items before accepting a collect quest counts on activation.
- [ ] Save mid-stage, change the quest data (add stage, reorder), load: progress is preserved.
- [ ] Debug commands: `quest.start id`, `quest.setstage id stage`, `quest.complete id`.
