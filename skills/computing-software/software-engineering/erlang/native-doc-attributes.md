---
id: computing-software.software-engineering.erlang.native-doc-attributes
name: native-doc-attributes
category: computing-software
field: software-engineering
product: erlang
tags: [erlang, erl-docs, native-doc-attributes]
level: practitioner
status: draft
description: "Erlang/OTP 27 native documentation: -moduledoc and -doc attributes with Markdown, doc false and shell h/1."
sources:
  - https://www.erlang.org/doc/apps/tools/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# -moduledoc and -doc attributes
**Goal:** document modules in code with the OTP 27 attributes.

```erlang
-module(calc).
-moduledoc """
Small calculator.

Supports `add/2`.
""".
-export([add/2]).
-doc "Add two numbers.".
-spec add(number(), number()) -> number().
add(A, B) -> A + B.
-doc false.
-export([internal/0]).
```
- Available from OTP 27: text is Markdown; the docs are stored in the BEAM file and shown by `h(calc)` and `h(calc, add)` in the shell.
- `-doc #{since => "1.2"}.` attaches metadata (exact metadata keys per the docs).
- `-doc false.` hides an exported function from documentation.
- The same attributes feed ExDoc to build HTML.

## Gotchas
- Older OTP releases fail to compile these attributes; guard with `-ifdef(OTP_RELEASE)` and a release check if you support them (check `?OTP_RELEASE >= 27`).

## Self-check
Document a function, compile, and call `h(calc, add)` in the shell.
