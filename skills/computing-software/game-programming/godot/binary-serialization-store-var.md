---
id: computing-software.game-programming.godot.binary-serialization-store-var
name: binary-serialization-store-var
category: computing-software
field: game-programming
product: godot
tags: [godot, godot-save-game, store_var, var_to_bytes, binary-save, game-programming]
level: practitioner
status: verified
description: "Serialize Godot data in binary with store_var/get_var and var_to_bytes/bytes_to_var: supported types, object decoding risks, versioning, compression and network payloads."
sources: ["https://docs.godotengine.org/en/stable/classes/class_fileaccess.html#class-fileaccess-method-store-var", "https://docs.godotengine.org/en/stable/tutorials/io/binary_serialization_api.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Binary serialization with store_var and var_to_bytes

**Goal:** compact, fast save/network payloads using Godot's Variant binary format, without opening a
code-execution hole.

## API
```gdscript
var f := FileAccess.open("user://world.bin", FileAccess.WRITE)
f.store_32(SAVE_VERSION)
f.store_var({"pos": player.global_position, "inv": inventory_dict, "seed": world_seed})
f.close()

var r := FileAccess.open("user://world.bin", FileAccess.READ)
var version := r.get_32()
var data = r.get_var()           # allow_objects defaults to false
```
`var_to_bytes(value)` / `bytes_to_var(bytes)` produce/consume `PackedByteArray` (for network or
embedding). `var_to_bytes_with_objects` / `bytes_to_var_with_objects` encode full Objects.
Without the flag, `get_var()` on an encoded object logs `ERR_UNAUTHORIZED` and returns null.

## Supported natively
All Variant types: ints, floats, strings, Vector2/3/4, Transform, Color, arrays, dictionaries, packed
arrays, NodePath, StringName. Format documented in "Binary serialization API" (type header + data,
little-endian, 4-byte aligned).

## Objects: don't
`store_var(obj, true)` / `get_var(true)` serialize objects **including their script**; decoding a file
from an untrusted source can instantiate arbitrary scripts = code execution. Keep `allow_objects`
false for saves and network data; convert objects to dictionaries yourself.

## Versioning
Binary Variant data has no schema. Write a version first, store dictionaries with string keys (not
positional arrays) so fields can be added, and migrate by version on load.

## Size and compression
- Floats are 32-bit unless the value needs double: `var_to_bytes(1.5)` is 8 bytes, `var_to_bytes(0.1)` is 12 and
  round-trips exactly. Ints are 8 bytes when they fit in 32 bits (`5`) and 12 otherwise (`5000000000`).
  A `Vector2` is 12 bytes in a default (single-precision) build.
- Compress: `bytes.compress(FileAccess.COMPRESSION_ZSTD)` + store the uncompressed size for
  `decompress(size, mode)`, or `FileAccess.open_compressed(path, mode, COMPRESSION_ZSTD)`.

## Compared to alternatives
| Format | Pros | Cons |
|---|---|---|
| JSON | readable, tool-friendly | floats as text, no Vector types (convert), larger |
| store_var | compact, all Variant types | opaque, Godot-only |
| Resources (.tres/.res) | editor integration | can embed scripts -> unsafe for user files |

## Gotchas
- `get_var` on a truncated file returns null with an error; validate types after loading
  (`typeof(data) == TYPE_DICTIONARY`).
- Random bytes passed to `bytes_to_var` mostly fail with errors; in a 2,000-buffer fuzz run two decoded to an
  `EncodedObjectAsID` (an object-id placeholder with no script), never a script instance. Still validate the type.
- Test saves across Godot upgrades; the format is documented but not versioned by the engine.

## Verify
- [ ] Load a save written by the previous version through the migration path.
- [ ] Fuzz: random bytes passed to `bytes_to_var` never yield a script-bearing object (`get_script() == null` on any Object result).
## Checked
Ran on Godot 4.7.2 headless: `store_32` plus `store_var` round trip of a Dictionary with Vector2/int/float/large int; encoded sizes quoted above; `store_var(obj, true)` then `get_var()` returns null with `ERR_UNAUTHORIZED` and `get_var(true)` returns the object; `var_to_bytes_with_objects` works and `bytes_to_var` refuses it; truncated file returns null with a size error; ZSTD `compress`/`decompress(size, mode)` (1028 bytes to 36 and back) and `open_compressed` round trip; 2,000-buffer fuzz result as stated. The "4-byte header, little-endian, padded to 4 bytes" format description is from the Binary serialization API page in the Godot docs.
