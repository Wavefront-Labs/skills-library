---
id: computing-software.software-engineering.d.d-output-ranges-and-custom-algorithms
name: d-output-ranges-and-custom-algorithms
category: computing-software
field: software-engineering
product: d
tags: [d-output-ranges-and-custom-algorithms, ranges, output-range, put, appender, sink, formattedwrite, range-generic, isoutputrange, d]
level: advanced
status: draft
description: "Use output ranges (put) and Appender, write generic range algorithms with constraints and ElementType, and sink-style APIs like std.format formattedWrite."
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

# Output ranges, Appender and writing range-generic algorithms

Goal: write allocation-friendly APIs.

- An output range is anything with `put(x)`: arrays (`put` appends only if you manage slice shrinking), `Appender!(T[])`, `File.lockingTextWriter`, `OutBuffer`, and your own struct with `void put(T x)`.
- Pattern: take a sink instead of returning a string:
```d
void toText(W)(ref W w, int x) if (isOutputRange!(W, char)) {
    import std.format : formattedWrite;
    w.formattedWrite("<%d>", x);
}
auto app = appender!string; toText(app, 5); app.data;
```
- `std.range.put(r, x)` handles ranges of chars/elements; `isOutputRange!(R, E)`.
- Writing algorithms: constrain with `isInputRange!R`, use `ElementType!R`, `isRandomAccessRange` branches via `static if` for speed, return lazy range structs with `save` for forward sources.
- `NullSink` discards (`std.range.primitives`, `nullSink`), `tee` splits.

Gotchas:
- Passing an Appender by value copies the handle; pass `ref`.
- Don't hold `.data` across further `put`.

Verify: unittest feeding both an `Appender` and a `File.lockingTextWriter`-like sink gives the same text.
