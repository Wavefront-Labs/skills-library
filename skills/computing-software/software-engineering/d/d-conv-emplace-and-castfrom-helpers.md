---
id: computing-software.software-engineering.d.d-conv-emplace-and-castfrom-helpers
name: d-conv-emplace-and-castfrom-helpers
category: computing-software
field: software-engineering
product: d
tags: [d-conv-emplace-and-castfrom-helpers, std-conv, emplace, castfrom, roundto, tochars, asoriginaltype, std-conv-helpers, allocation-free-conversion, d]
level: advanced
status: draft
description: "Use emplace to construct in raw memory, castFrom!T.to!U checked casts, roundTo!int for rounding conversions, and toChars/asOriginalType for allocation-free conversion."
sources:
  - https://dlang.org/spec/spec.html
  - https://dlang.org/phobos/index.html
  - https://dub.pm/
  - https://ddili.org/ders/d.en/index.html
  - https://dlang.org/articles.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# emplace, castFrom, roundTo and other std.conv helpers

Goal: use the less-known conversion tools.

- `emplace!T(void[] mem, args)` constructs an object in place (classes and structs; for classes `mem.length >= __traits(classInstanceSize, C)`), returns a reference/pointer; follow with `destroy` manually. `emplace(&slot, args)` for typed slots.
- `castFrom!long.to!int(x)` performs a checked cast with the source type stated (documents intent, throws on overflow, safe for `@safe` code).
- `roundTo!int(2.5)` rounds to nearest (ties away from zero, check `std.math.lrint`/`round` semantics); `to!int(2.5)` truncates.
- `toChars!10(n)` returns a lazy range of digits, no GC allocation (`toChars!(16, char, LetterCase.upper)(255)`); `.array` or copy into a buffer.
- `asOriginalType(enumValue)` yields the base value of an enum without cast; `OriginalType!E`.
- `to!(const(char)*)` is not available; use `toStringz` (std.string).
- `std.conv.emplaceRef` used for ranges; `std.conv.to!` of `Nullable` unwraps.

Gotchas:
- `emplace` does not zero or register memory with the GC; if the object holds GC pointers in malloc'd memory, call `GC.addRange`.
- Misusing `castFrom` with the wrong declared source type is a compile error, which is the point.

Verify: unittest checking `toChars!2(5).array == "101"` and a checked cast throwing on overflow.
