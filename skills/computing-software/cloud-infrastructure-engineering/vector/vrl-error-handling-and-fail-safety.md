---
id: computing-software.cloud-infrastructure-engineering.vector.vrl-error-handling-and-fail-safety
name: vrl-error-handling-and-fail-safety
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [vrl, errors, fallible, abort, coalesce, type-safety, vector]
level: advanced
status: docs-checked
description: "Handle fallible VRL functions with the bang form, error assignment or coalescing to satisfy the compiler."
sources:
  - https://vector.dev/docs/reference/vrl/
  - https://vector.dev/docs/reference/vrl/expressions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A VRL program will not compile unless every error from a fallible function is handled. The compiler also checks types. Together these force an explicit decision about malformed data instead of surprising you in production.

Three ways to handle a fallible call:

```coffeescript
# 1. Abort the program if it fails (the ! suffix)
parsed = parse_json!(string!(.message))

# 2. Capture the error in a second target
.parsed, .err = parse_json("malformed")

# 3. Coalesce with a fallback using ??
.msg = parse_syslog(.message) ?? parse_common_log(.message) ?? "malformed"
```

With `!`, an error aborts the whole program. Type safety is progressive: a field starts as unknown, so `downcase!(.foo)` needs `!` because `.foo` might not be a string. Once assigned, VRL knows `.foo` is a string and `upcase(.foo)` needs no `!`.

The `abort` expression terminates the program and discards modifications; an optional message appears in dropped-event metadata. What happens to the event afterwards is set on the transform (see remap-transform-behaviour).

Choose per field: `!` when the event is useless without it, error assignment when you can still ship the event with a marker, coalescing when there is a safe default.

Verify using `vector vrl` with inputs that are valid and invalid.

## Checked

2026-11-03. Read reference/vrl and reference/vrl/expressions. Confirmed: fallible functions must be handled at compile time, the `!` abort form, error assignment to a second target, `??` coalescing, progressive type safety, and `abort` with an optional message included in dropped-event metadata. Nothing removed.

Method: documentation only; no commands were run.
