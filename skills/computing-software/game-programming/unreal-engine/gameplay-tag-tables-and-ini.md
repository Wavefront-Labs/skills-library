---
id: computing-software.game-programming.unreal-engine.gameplay-tag-tables-and-ini
name: gameplay-tag-tables-and-ini
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, ue5, gameplay-tags, gameplay-tag-table, defaultgameplaytags-ini, tag-sources, project-settings, game-programming]
level: intro
status: draft
description: "Manage gameplay tag definitions: Project Settings and DefaultGameplayTags.ini, extra tag ini files per plugin, Gameplay Tag Table data tables, tag sources and restricted tags."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/using-gameplay-tags-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/gameplay-tags-project-settings-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Gameplay tag tables and ini management

**Goal:** a tag list that scales across teams and plugins without merge conflicts in one giant file.

## Ways to define tags
1. **Project Settings > Project > GameplayTags > Manage Gameplay Tags**: writes to
   `Config/DefaultGameplayTags.ini`:
```ini
[/Script/GameplayTags.GameplayTagsSettings]
ImportTagsFromConfig=True
FastReplication=True
+GameplayTagList=(Tag="Status.Debuff.Stun",DevComment="Prevents movement and abilities")
+GameplayTagList=(Tag="Damage.Fire",DevComment="")
```
2. **Extra ini sources**: add tag source files under `Config/Tags/` (e.g. `Config/Tags/Combat.ini`,
   `Config/Tags/UI.ini`) with the same section format. When adding a tag in the editor choose the
   **Tag Source** to write to. Splitting by area avoids merge conflicts.
3. **Plugins**: `Plugins/MyPlugin/Config/Tags/MyPluginTags.ini` is loaded with the plugin (game feature plugins too).
4. **Gameplay Tag Table**: DataTable with row struct `GameplayTagTableRow` (Tag, DevComment), listed in
   Project Settings > Gameplay Tag Table List. Import from CSV: handy for designer-owned lists.
5. **Native tags** in C++ (for tags code depends on).

## Settings worth knowing
- **Fast Replication**: tags replicate as indices; server and clients must have identical tag sets.
  `NumBitsForContainerSize`, `NetIndexFirstBitSegment` tune size.
- **Restricted tags** (`DefaultGameplayTagsRestricted.ini` / restricted tag sources): only listed owners can
  add children; protects top-level hierarchies.
- **Warn On Invalid Tags**, **Clear Invalid Tags** (remove references to deleted tags on load).
- `CommonlyReplicatedTags`: a list sent with the fewest bits.

## Hygiene
- Agree a hierarchy up front: `Ability.*`, `Status.*`, `Damage.*`, `Cue.*` (GameplayCue tags must start with `GameplayCue.`), `Input.*`, `Event.*`.
- Add DevComments; the tag picker shows them as tooltips.
- Before deleting, use the tag manager's **Search for References**.
- Renames need redirects (see gameplay tag redirects).

## Verify
- [ ] Tag ini files are split per area; no two branches edit the same file for unrelated features.
- [ ] Client and server builds load the same tag set (fast replication mismatch logs warnings).
