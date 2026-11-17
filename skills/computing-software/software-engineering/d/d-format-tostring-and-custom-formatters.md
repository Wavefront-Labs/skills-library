---
id: computing-software.software-engineering.d.d-format-tostring-and-custom-formatters
name: d-format-tostring-and-custom-formatters
category: computing-software
field: software-engineering
product: d
tags: [d-format-tostring-and-custom-formatters, std-format, tostring, formattedread, unformatvalue, custom-formatter, text, formatspec, sink-tostring, std-conv-text, d]
level: advanced
status: docs-checked
description: "Control how your types print via toString overloads, parse with formattedRead/unformatValue, and use std.conv text/to!string next to format."
sources:
  - https://dlang.org/phobos/std_format_write.html
  - https://dlang.org/phobos/std_format_read.html
  - https://dlang.org/phobos/std_conv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom toString, formattedRead and text/to-string conversions

Goal: customise printing and parsing.

- A struct, union, class or interface may define `toString` in these forms: `void toString(Writer, Char)(ref Writer w, const ref FormatSpec!Char fmt)` (the function decides which format characters it accepts), `void toString(Writer)(ref Writer w)`, `string toString()`. Where a template is not possible (for example overriding `Object.toString`) the slower sink forms exist: `void toString(void delegate(const(char)[]) sink, const ref FormatSpec!char fmt)`, `(sink, string fmt)` and `(sink)`.
- Precedence: Writer versions first, then sink versions, with `string toString()` last. A plain `string toString()` is only used with `%s`.
- Inside a `toString` with a spec, call `formatValue(writer, x, fmt)` (or `sink.formatValue(x, fmt)`) so that width and flags such as `%03d` apply to each field, giving `(016,011)` for the page's `Point2` example.
- With no `toString`: an input range is formatted like a range; an `alias this` builtin like that builtin; otherwise a struct prints `Type(field1, field2, ...)`, a class its fully qualified name and a union its base name.
- Enums print the member name with `%s` (`cast(A)3` for an unnamed value) and like their base value with other format characters (`%d` gives the number).
- Reading: `import std.format : formattedRead; string w; int n; "apples 7".formattedRead!"%s %d"(w, n);` returns the number of variables filled (fewer if the input ends early). The `formattedRead!(string, int)("%s %d")` template form returns a tuple and throws `FormatException` if input ends early. A space in the format matches any run of whitespace. `%*d` (also `u` and `c`) skips a value. `unformatValue!T(input, spec)` reads a single value with a `singleSpec` spec.
- `std.conv.text(a, b, c)` joins the string forms of its arguments without a format string; `to!string(x)` converts one value.
- Output into a caller-supplied buffer: `char[64] buf; auto s = sformat!"%d"(buf[], 5);` (the page notes allocations can still occur in some cases).

Gotchas:
- Only `%s` reaches `string toString()`; the compound and other format characters need the spec-taking forms.
- `formattedRead` fills as many variables as the input allows; check the returned count.

Verify: unittest asserting `format("%s", p)` for each `toString` form you define.

## Checked

2026-11-08. Confirmed against std.format.write (toString signatures, precedence, fallback formatting, enum behaviour, `formatValue`, `formattedWrite`), std.format.read (`formattedRead` overloads, return values, whitespace and `*` skipping, `unformatValue`) and std.conv (`text`, `to`).

Removed because the pages did not confirm it: the claim that `string toString()` allocates and the sink form avoids it, Nullable printing, `leftJustify`/`rightJustify`, the claim that extra input is left in the string argument, and the speed advantage of `text` over `format`. The description was edited to drop the performance wording. Replaced landing-page sources with the three pages above.

Method: documentation only; no commands were run.
