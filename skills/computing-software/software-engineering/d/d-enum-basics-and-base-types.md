---
id: computing-software.software-engineering.d.d-enum-basics-and-base-types
name: d-enum-basics-and-base-types
category: computing-software
field: software-engineering
product: d
tags: [d-enum-basics-and-base-types, enums, enum, enummembers, enum-base-type, enum-to-string, flags-enum, std-conv-enum, d]
level: intro
status: docs-checked
description: "Define D enums with explicit base types and values, iterate members with EnumMembers, convert by name with std.conv.to, and use .min .max .init."
sources:
  - https://dlang.org/spec/enum.html
  - https://dlang.org/phobos/std_conv.html
  - https://dlang.org/phobos/std_traits.html
  - https://dlang.org/phobos/std_typecons.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Named enums, base types, .min .max and conversions

Goal: use enums with exhaustive handling.

```d
enum Color : ubyte { red, green = 5, blue }
import std.traits : EnumMembers; import std.conv : to;
foreach (c; EnumMembers!Color) writeln(c, " ", cast(int)c);
auto c = "green".to!Color;      // throws ConvException if unknown
string s = Color.blue.to!string;
```
- Base type after the colon; if omitted it is the type of the first member's initialiser, else `int`. An unassigned member is the previous value plus one.
- `Color.min`, `Color.max`, `Color.init` (first member).
- A named enum member converts implicitly to its base type, but the base type needs an explicit `cast(Color)i` to become the enum.
- Flags: `std.typecons.BitFlags!E` works on enums whose members are bit flags (`isBitFlagEnum!E`).
- `final switch` enforces exhaustiveness.

Gotchas:
- Overflow is an error: if the previous member is its type's `.max`, an implicit next value is a compile error.
- `"green".to!Color` is case-sensitive.

Verify: unittest round-trips every member via to!string and to!Color.

## Checked
Checked 2026-11-03 against the D spec Enums page and the std.conv, std.traits (`EnumMembers`) and std.typecons (`BitFlags`) pages. Confirmed: base type rules, `.init`/`.min`/`.max`, implicit enum-to-base and explicit base-to-enum casts, string conversion by symbolic name, case-sensitive parse with `ConvException`, `final switch`. Removed: the duplicate-value and invalid-cast remarks.

Method: documentation only; no commands were run.
