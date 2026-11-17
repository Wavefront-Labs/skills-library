---
id: computing-software.software-engineering.zig.json-parse-stringify
name: json-parse-stringify
category: computing-software
field: software-engineering
product: zig
tags: [zig, json-parse-stringify, zig-std-json, parsefromslice, std-json, json-value, stringify]
level: practitioner
status: docs-checked
description: "Parse JSON into Zig structs with std.json.parseFromSlice, read dynamic Value trees, and serialise with stringify options."
sources:
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/json.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/json/static.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/json/Stringify.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/json/Scanner.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parsing and writing JSON
**Goal:** (de)serialise JSON safely.

```zig
const Config = struct { name: []const u8, port: u16 = 8080, tags: []const []const u8 = &.{} };
const parsed = try std.json.parseFromSlice(Config, alloc, text, .{ .ignore_unknown_fields = true });
defer parsed.deinit();                                // frees all strings
std.debug.print("{s}:{d}\n", .{ parsed.value.name, parsed.value.port });

const tree = try std.json.parseFromSlice(std.json.Value, alloc, text, .{});
defer tree.deinit();
const port = tree.value.object.get("port").?.integer;

const out = try std.json.Stringify.valueAlloc(alloc, parsed.value, .{ .whitespace = .indent_2 });
defer alloc.free(out);
```
- Types map: struct to object, `?T` to nullable, slices to arrays, enums to strings, tagged unions to single-key objects.
- `parseFromSliceLeaky` with an arena avoids the `Parsed.deinit` bookkeeping.
- Errors include `error.UnexpectedToken`, `MissingField`, `UnknownField`, `Overflow`.
- Streaming: `std.json.Scanner` / `Reader` for large documents.
- Writing in 0.15.1: `std.json.Stringify.valueAlloc(gpa, value, options)` returns `[]u8`, `Stringify.value(v, options, writer)` writes to a writer, and `std.json.fmt(value, options)` wraps a value for formatting. `stringifyAlloc` does not exist.
- Custom (de)serialisation: add `jsonParse`/`jsonStringify` methods to the type.

## Gotchas
- Input size is not limited by the parser: cap `max_value_len` and the input length for untrusted data.
- Strings in `Parsed.value` die at `deinit`; copy what you keep.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference and the 0.15.1 standard-library source (tag 0.15.1). Confirmed: `parseFromSlice`, `parseFromSliceLeaky`, `ParseOptions`, `Parsed`, `Value`, `Scanner`, `Reader`, `default_max_value_len`, `Stringify.valueAlloc`, `Stringify.value`, `Options.whitespace` (`.indent_2`), `std.json.fmt`. Fixed: `std.json.stringifyAlloc` does not exist in 0.15.1 (the example now uses `Stringify.valueAlloc`). Removed: the claim that strings are copied by default.

Method: documentation only; no commands were run.

## Self-check
Round-trip a struct with an optional field and slice; assert equal after parse(stringify(x)).
