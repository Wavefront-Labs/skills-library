---
id: computing-software.game-programming.unreal-engine.gameplay-tag-fast-replication
name: gameplay-tag-fast-replication
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, fast-replication-tags, gameplay-tags, replication, net-index, bandwidth, game-programming]
level: practitioner
status: draft
description: "Enable Unreal fast gameplay tag replication: net index ordering, CommonlyReplicatedTags, NetIndexFirstBitSegment tuning, and keeping server and client tag lists identical."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/using-gameplay-tags-in-unreal-engine", "https://docs.unrealengine.com/5.3/en-US/API/Runtime/GameplayTags/UGameplayTagsSettings/", "https://github.com/tranek/GASDocumentation"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fast gameplay tag replication

**Goal:** replicated tags and containers cost a few bits instead of full names.

## Settings (Project Settings > GameplayTags, `DefaultGameplayTags.ini`)
```ini
[/Script/GameplayTags.GameplayTagsSettings]
FastReplication=True
NumBitsForContainerSize=6
NetIndexFirstBitSegment=16
+CommonlyReplicatedTags=Status.Dead
+CommonlyReplicatedTags=Ability.Block
```
- **FastReplication**: tags serialize as a net index (position in the sorted tag list) instead of
  their name. Requires server and client to have the identical tag dictionary.
- **CommonlyReplicatedTags**: placed at the start of the index table so they fit in the first bit
  segment.
- **NetIndexFirstBitSegment**: bits for the first segment; tags beyond need extra bits. Tune using
  the tag count printed by `GameplayTags.PrintReplicationIndices` and frequency from
  `GameplayTags.PrintReplicationFrequencyReport`.
- **NumBitsForContainerSize**: max tags per replicated container = 2^N - 1.

## Requirements
- Every tag must be known at startup on both sides: ini, data tables, native tags. Tags added at
  runtime with `AddNativeGameplayTag` late, or loaded via plugins only on one side, desync indices.
- Clients and servers must run the same build/content version; a mismatched tag list mis-decodes
  silently (wrong tags, not errors). The hash check (`GameplayTagsManager` net hash) logs mismatches.

## Gotchas
- Game Feature plugins that add tags must be loaded on both sides before replication, or keep their
  tags in base ini.
- Changing tag lists in a patch requires all clients to update.
- Replicating large containers often: prefer replicating a bitmask struct or a few tags.

## Verify
- [ ] Network Insights shows tag containers serialized in bits, not strings.
- [ ] `PrintReplicationIndices` output matches on a server and a client build.
