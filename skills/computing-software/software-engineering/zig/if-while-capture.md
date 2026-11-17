---
id: computing-software.software-engineering.zig.if-while-capture
name: if-while-capture
category: computing-software
field: software-engineering
product: zig
tags: [zig, if-while-capture, zig-control-flow, payload-capture, while-continue-expression, else-capture]
level: intro
status: docs-checked
description: "Use Zig if and while with optional and error-union captures, else branches, and continue expressions."
sources:
  - https://ziglang.org/documentation/0.15.2/
  - https://zig.guide/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# if/while with capture and else
**Goal:** unwrap optionals and error unions inline.

```zig
if (maybe) |v| { use(v); } else { none(); }           // ?T
if (res) |v| { use(v); } else |err| { handle(err); }  // E!T
while (it.next()) |item| { ... }                      // loops until null
while (i < n) : (i += 1) { ... }                      // continue expression
while (stack.pop()) |top| : (count += 1) { ... }
```
- Condition must be `bool`, optional or error union; there is no truthiness of integers.
- Capture by pointer to mutate in place: `if (opt) |*v| v.* += 1;`.
- `while (cond) |v| {...} else {...}`: else runs when the loop ends from the condition becoming false/null, not on `break`.
- `break` and `continue` work in both; `while` is an expression and can yield a value through `break value` with `else`.

## Gotchas
- Captures are const values; to modify the original use `|*v|`.
- Discard captures you do not use with `_`: `if (x) |_| {}`.

## Self-check
Iterate a `std.ArrayList` pop-loop until empty, summing values, and verify that else runs on exhaustion.

## Checked
- 2026-11-02: compared with the Zig 0.15.2 language reference (ziglang.org/documentation/0.15.2/).
- Confirmed: if/while captures, else |err|, continue expressions, pointer captures (language reference).
- Removed or changed: nothing.
- Not checked: std library calls in code examples (std.fs, std.mem, std.log, std.testing, std.meta) are illustrative and were not compared with the std API docs.
Method: documentation only; no commands were run.
