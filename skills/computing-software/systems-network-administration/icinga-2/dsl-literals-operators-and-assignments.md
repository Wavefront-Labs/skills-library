---
id: computing-software.systems-network-administration.icinga-2.dsl-literals-operators-and-assignments
name: dsl-literals-operators-and-assignments
category: computing-software
field: systems-network-administration
product: icinga-2
tags: [systems-network-administration, icinga-2, dsl, language-reference, literals, operators, duration, indexer, dollar-escape]
level: intro
status: docs-checked
description: "Icinga 2 DSL building blocks: duration, string and multi-line literals, dictionaries, arrays, operators, assignments, the dollar escape."
sources:
  - https://icinga.com/docs/icinga-2/latest/doc/17-language-reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DSL literals, operators and assignments
**Literals:** numbers are floating point (`27.3`). Durations take suffixes `ms`, `s`, `m`, `h`, `d` (`2.5m`) and become seconds. Strings use `"..."` with escapes `\"`, `\\`, `\t`, `\r`, `\n`, `\b`, `\f`, and `$$` for a literal dollar (the `$` is reserved for runtime macros). Multi-line strings sit between `{{{` and `}}}` with no escaping. Also `true`, `false`, `null`.

**Dictionary:** unordered, unique case-sensitive keys, separated by commas or newlines. Quote keys that are not valid identifiers. **Array:** ordered, comma-separated, mixed types allowed. A trailing comma is optional in both.

**Operators** (descending precedence): grouping/call/subscript/dot; unary `!`, `~`, `+`, `-`, `&` (reference), `*` (dereference); `* / %`; `+ -` (`+` also concatenates strings); `<< >>`; `< > <= >=`; `in`, `!in`; `== !=`; `&`; `^`; `|`; `&&`; `||`; `=`; `=>`; ternary `?:`. `&&` and `||` return an operand, so `0 || 7` gives 7.

**Assignments:** `=`, `+=` (append to array or add), `-=`, `*=`, `/=`; each is shorthand for `a = a <op> b`.

**Indexer:** `hello.key = "world"` and `hello["key"] = "world"` set a dictionary element, equivalent to `hello += { key = "world" }`.

Reserved keywords such as `object`, `template` and `include` cannot be used as constants or custom variables.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Read the full page https://icinga.com/docs/icinga-2/latest/doc/17-language-reference/.
Fixed: backslash escape is written as a double backslash. No commands were run.
