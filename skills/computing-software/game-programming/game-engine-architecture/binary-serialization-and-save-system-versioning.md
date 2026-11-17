---
id: computing-software.game-programming.game-engine-architecture.binary-serialization-and-save-system-versioning
name: binary-serialization-and-save-system-versioning
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, serialization, save-system, versioning, schema-migration, binary-format, backward-compatibility, deserialization, endianness, forward-compatibility, save-corruption, checksum, game-programming, atomic-file-write]
level: advanced
status: draft
description: "Design a binary serializer and save-file schema that survives shipped patches adding, removing, or changing fields without breaking old save files."
sources: ["https://gafferongames.com/post/serialization_strategies/", "https://docs.unrealengine.com/en-US/saving-and-loading-your-game-in-unreal-engine"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Binary serialization and save-system versioning

**Goal:** write engine-level serialization for save files (and network
snapshots/replays, which share the same problem) that a patch 6 months later
can still read without corrupting or rejecting every player's existing save.
This is the infrastructure layer — the design-level question of *what counts
as game state and when to write it* belongs to gameplay programming, not here.

## The core mistake: serializing struct layout directly
`fwrite(&playerStruct, sizeof(playerStruct), 1, file)` works until you add a
field to `PlayerStruct` in the next patch — every existing save file is now the
wrong size/layout and either crashes on read or silently reads garbage into the
new field. Binary serialization for anything that outlives a single build must
be **field-tagged, not layout-dependent**: write each field with an explicit ID
(or write a count + loop), so a reader can skip fields it doesn't recognize
(old reader, new save — ignore the extra field) and default fields it doesn't
find (new reader, old save — use the field's default instead of reading
uninitialized/misaligned bytes). This is the same problem Protocol Buffers and
FlatBuffers solve generically; an engine can roll a minimal version of the same
idea (tag + length + value chunks) without pulling in a full schema compiler.

## Version the file, not just the field
Every save file starts with a header: a magic number (quick corruption/wrong-
file-type check) and a **version integer**. On load, branch on version to run
**migration steps** — not "if old version, special-case every read forever,"
but a chain: load as v1 → apply v1→v2 migration (add default value for a new
field, rename a key) → apply v2→v3 → ... → current. Each migration step is
small, tested once, and composes — this is strictly easier to maintain than a
reader with nested version checks scattered through every field read. Bump the
version on **any** change to the format, even ones that feel backward-
compatible ("I only added a field with a sensible default") — the alternative
is a silent gap in migration coverage discovered only when a specific old save
hits it in the wild.

## Corruption and partial writes
A save interrupted mid-write (crash, power loss, console suspend) must not
destroy the previous good save. Standard pattern: write to a **temporary file**,
`fsync`/flush, then atomically rename over the real save file (an OS-level
rename is atomic; an in-place overwrite is not). Add a checksum (CRC32 is
enough; it's integrity, not security) covering the payload, checked on load —
a failed checksum means "fall back to the last-known-good backup slot," not
"crash the game." Keep at least one rotating backup slot for exactly this case;
players losing hours of progress to a corrupted single save file is one of the
most reputationally damaging bugs a game can ship.

## Endianness and alignment (less common now, still bites cross-platform)
If a save/replay file written on one platform is read on another with
different endianness (rare today but real for some console/PC cross-save, and
for network snapshots between heterogeneous hardware), raw multi-byte integers
read back reversed. Serialize integers through explicit
host-to-network/fixed-endian helper functions, never by casting a struct
pointer to bytes, if the format might ever cross platforms.

## Verify
- [ ] Added a field to a test save struct, confirmed an old-format save file
      still loads (missing field gets its default) and a new save still loads
      in logic that predates the field (field is ignored, not misread).
- [ ] Save version bumped and a migration step written for every format change,
      not just "breaking" ones.
- [ ] Killing the process mid-save (pull power/kill -9 during write) leaves the
      previous save file intact and loadable.
- [ ] Checksum mismatch triggers fallback-to-backup, verified by corrupting a
      byte in a save file and confirming the game doesn't crash on load.
