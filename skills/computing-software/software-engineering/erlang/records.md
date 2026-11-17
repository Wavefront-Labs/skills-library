---
id: computing-software.software-engineering.erlang.records
name: records
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-maps-records, records]
level: practitioner
status: docs-checked
description: "Erlang records: -record definitions, field defaults, update syntax, record_info, sharing via .hrl and why maps are preferred across API boundaries."
sources:
  - https://www.erlang.org/doc/system/reference_manual.html
  - https://www.erlang.org/doc/apps/stdlib/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Records and record_info
**Goal:** use records for fixed-shape internal state.

```erlang
-record(user, {id :: integer(), name = <<>> :: binary(), tags = [] :: [atom()]}).
U = #user{id = 1},
Name = U#user.name,
U2 = U#user{name = <<"ann">>},
#user{id = Id} = U2,
record_info(fields, user).         % [id,name,tags]
```
- Record expressions are translated to tuple expressions at compile time, so `#user{}` is a tuple `{user, Id, Name, Tags}`. `record_info(size, user)` is one more than the number of fields.
- A field without a default is `undefined`. A default is an expression that must not use variables.
- A record definition must come before its first use. If several modules use a record, put the definition in an include file (`.hrl`).
- The Efficiency Guide advises using records only within a unit of code that can be recompiled all at once (one application or module): adding a field means all code using the record must be recompiled. Across API boundaries prefer maps or accessor functions.
- In the shell, `rr(File)` reads record definitions from a file so terms print as records (from OTP 26 records can also be defined in the shell with the normal syntax).

## Gotchas
- Field names are checked at compile time (a misspelled field is a compile error), unlike map keys.

## Self-check
Define a record, print a value in the shell before and after `rr/1`.

## Checked
2026-11-02. Erlang Reference Manual "Records" (definition syntax, defaults, record_info, translation to tuples, OTP 26 shell definitions), Efficiency Guide "Maps" (records vs maps, recompilation advice), STDLIB shell help text (rr/1). Removed: claims about stored terms, hot upgrades, Dialyzer and ETS/Mnesia migration (not in these pages).
Method: documentation only; no commands were run.
