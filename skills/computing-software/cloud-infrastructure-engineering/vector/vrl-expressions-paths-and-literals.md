---
id: computing-software.cloud-infrastructure-engineering.vector.vrl-expressions-paths-and-literals
name: vrl-expressions-paths-and-literals
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [vrl, expressions, assignment, regex, strings, timestamps, vector]
level: practitioner
status: docs-checked
description: "Use VRL assignment forms, literal sigils, object merge and array-to-events behaviour correctly."
sources:
  - https://vector.dev/docs/reference/vrl/expressions/
  - https://vector.dev/docs/reference/vrl/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Everything in VRL is an expression that returns a value.

**Assignment.** To a path (`.message = "Hi"`, `.parent.child = 1`, `.array[1] = "x"`) or a variable. Merge objects with `|=`:

```coffeescript
my_variable = {"message": "Hello, World!"}
my_variable |= {"level": "info"}
```

**Literals.** Regular expressions use the `r` sigil with Rust regex syntax, flags like `(?i)` and named captures, for example `r'(?P<y>\d{4})-(?P<m>\d{2})'`. Timestamps use `t'2021-02-11T10:32:50.553955473Z'` in RFC 3339 form. Raw strings use `s'...'`; double-quoted strings interpret escapes and can be templated with `{{ var }}` where the variable must be a string. Strings concatenate with `+`.

**Objects** order keys alphabetically, so JSON encoding is key-sorted.

**Functions.** Arguments may be positional or named; closures are used by iterating functions, e.g. `for_each(...) -> |index, value| { ... }`.

**Event shape.** `.` can be reassigned. Setting it to an array makes the remap transform emit one event per element, and non-object elements become `{"message": element}`.

```coffeescript
. = ["hello", 1, true, {"foo": "bar"}]
```

This emits four events. Use it to split batched payloads.

## Checked

Method: docs-checked 2026-11-09 against the Vector VRL expressions page (raw markdown) and the cue definitions it renders (assignment, function call, event, regular expression, string, timestamp and object literals in the vectordotdev/vector repo). Dropped an unsourced verification line. `|=` is only valid when both sides are objects.
