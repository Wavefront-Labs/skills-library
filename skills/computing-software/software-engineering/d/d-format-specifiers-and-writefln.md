---
id: computing-software.software-engineering.d.d-format-specifiers-and-writefln
name: d-format-specifiers-and-writefln
category: computing-software
field: software-engineering
product: d
tags: [d-format-specifiers-and-writefln, std-format, format, writefln, specifiers, positional-args, array-format, formattedwrite, format-specifiers, d]
level: practitioner
status: docs-checked
description: "Use std.format specifiers (%s %d %f %x %b %o %e %g %c), flags (0 - + space #), width, precision, positional %1$s, and array/range formats %(%s, %)."
sources:
  - https://dlang.org/phobos/std_format.html
  - https://dlang.org/phobos/std_stdio.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# format specifiers: %s %d %f %x %e %( %) and widths

Goal: format values predictably.

- Basic: `format("%s has %d items costing %.2f", name, n, price)` returns a string; `writefln` prints (equivalent to `writef` plus a newline); `sformat(buf, ...)` writes into a char buffer you supply (a `RangeError` if it is too small; the page notes it can still allocate on exceptions and in allocating `toString` functions); `formattedWrite(sink, ...)` writes to an output range.
- Format characters: `%s` human readable form (any type), `%d` signed decimal, `%u` unsigned decimal, `%x`/`%X` hex, `%o` octal, `%b` binary, `%f`/`%F` natural, `%e`/`%E` scientific, `%g`/`%G` short notation, `%a`/`%A` hex float, `%c` character, `%r` raw bytes, `%%` a percent sign. The default floating point precision is 6 digits.
- Flags: `-` left justify, `=` centre, `+` or space sign, `0` zero fill, `#` alternative form (`%#x` gives `0x` prefix). Width and precision: `%05d`, `%-10s`, `%10.3f`, `%*d` (width from an argument), `%.*f` (precision from an argument). For integers precision is the minimum digit count; for strings and compounds it is the maximum number of elements.
- Grouping: `%,3d` groups digits (`%,3?d` takes the separator from an argument).
- Positional: `%2$s %1$s` reorders arguments.
- Compound (arrays, ranges): `%(%s, %)` formats each element, with the text after the element specifier used as the delimiter; `%|` marks where the delimiter starts; nested for matrices `%(%(%d %) - %)`. Strings and chars inside `%(` are quoted and escaped; use `%-(` to avoid that.
- Associative arrays: `%s` prints `[key:value, ...]` in unpredictable order; a compound uses two specifiers, key then value, which positional arguments can swap (`%(%2$s (%1$s), %)`).
- A struct without `toString` prints as `StructType(field1, field2, ...)`; one with an applicable `toString` uses it.
- Compile-time checked: `format!"%s %d"(a, b)` verifies the format string against the argument types and is slightly faster.

Gotchas:
- A spec and argument mismatch throws `FormatException` for the runtime form (`format("%d", "foo")`).
- Arrays of characters print as text; other arrays print in square brackets with a comma and space between elements.
- No localization; rounding follows the floating point unit's mode.

Verify: unittest `assert(format("%05.1f|%-4s|%x", 3.14159, "ab", 255) == "003.1|ab  |ff");`

## Checked

2026-11-08. Confirmed against the std.format page: format string grammar, format characters, flags, width/precision/separator, positional arguments, compound indicators and `%-(`, the type table (arrays, associative arrays, structs), `format`, `sformat` and their compile-time forms, `FormatException`. From std.stdio only the `writefln` entry was read.

Removed because the page did not confirm it: the `%(%s: %s, %)` over `byKeyValue` mapping claim, the `toString` sink signatures, and the "nogc friendly" wording (replaced by the page's caveat). Replaced landing-page sources with std.format and std.stdio.

Method: documentation only; no commands were run.
