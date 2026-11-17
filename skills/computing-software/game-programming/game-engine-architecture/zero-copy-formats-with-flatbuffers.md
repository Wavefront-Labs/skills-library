---
id: computing-software.game-programming.game-engine-architecture.zero-copy-formats-with-flatbuffers
name: zero-copy-formats-with-flatbuffers
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, flatbuffers, zero-copy, serialization, game-programming]
level: practitioner
status: draft
description: "Use FlatBuffers for zero-copy game data: schemas, flatc codegen, reading in place from mapped files, verifiers for untrusted data and schema evolution rules."
sources: ["https://flatbuffers.dev/", "https://github.com/google/flatbuffers"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Zero-copy formats with FlatBuffers

**Goal:** load game data (configs, levels, network messages) by mapping bytes and reading directly,
with no parse step or allocation.

## Schema
```fbs
namespace Game;
table Weapon { name:string; damage:float = 10; fire_rate:float; ammo:[ushort]; }
table WeaponDb { weapons:[Weapon]; }
root_type WeaponDb;
file_identifier "WPDB";
```
`flatc --cpp --gen-object-api weapons.fbs` generates accessors; `flatc -b weapons.fbs data.json`
converts designer JSON to binary in the build pipeline.

## Reading
```cpp
auto buf = mapFile("weapons.bin");                       // mmap or read into aligned memory
flatbuffers::Verifier v(buf.data(), buf.size());
if (!Game::VerifyWeaponDbBuffer(v)) fail();              // always for untrusted input (mods, network)
auto db = Game::GetWeaponDb(buf.data());
for (auto w : *db->weapons()) use(w->name()->c_str(), w->damage());
```
Accessors read offsets in place; strings and vectors point into the buffer. Keep the buffer alive
while you use the data.

## Evolution rules
- Add new fields only at the end of tables (or use explicit `(id: n)`); never remove (mark
  `(deprecated)`) or reorder; never change types.
- Defaults are not stored on the wire; changing a default changes old data's meaning.
- `struct` types are fixed layout, not evolvable; use for small math types (Vec3).

## Trade-offs
- Reads are slightly slower than native structs (offset indirection); copy hot data into engine
  structs if it's read every frame.
- Mutation is limited (in-place scalar mutation only); use the object API for editing tools.
- Alternatives: Cap'n Proto (similar), or custom "relocatable blob" formats with pointer fix-up.

## Verify
- Load time and allocations before/after vs JSON parsing; fuzz the verifier with corrupted files.
