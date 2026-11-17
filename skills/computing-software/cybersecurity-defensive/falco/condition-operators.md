---
id: computing-software.cybersecurity-defensive.falco.condition-operators
name: condition-operators
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [condition-syntax, comparison-operators, glob, regex, intersects]
level: practitioner
status: docs-checked
description: "Use Falco logical and comparison operators correctly: in versus intersects, contains, glob, exists, startswith and the RE2 POSIX regex."
sources:
  - https://falco.org/docs/concepts/rules/conditions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A condition is comparisons joined by `and`, `or`, `not`, with parentheses for precedence. Each comparison puts a field on the left and a value on the right: `evt.type = execve and (proc.name = cat or proc.name = grep)`.

Comparison operators:
- `=`, `==`, `!=` equality; `<=`, `<`, `>=`, `>` numeric.
- `contains`, `icontains` (case-insensitive), `bcontains`: substring; for flags, `evt.arg.flags contains O_TRUNC` tests that the flag is set.
- `startswith`, `bstartswith` (hexadecimal bytes, for example `evt.buffer bstartswith 012AB3CC`) and `endswith`.
- `exists`: the field is set, for example `k8s.pod.name exists`.
- `glob`, `iglob`: full-match glob, for example `fd.name glob "/home/*/.ssh/*"`.
- `in`: the left set is entirely contained in the right set. `(b,c,d) in (a,b,c)` is false because `d` is missing.
- `intersects`: at least one common element. `(b,c,d) intersects (a,b,c)` is true.
- `regex`: Google RE2 in POSIX mode (extended egrep syntax, no backreferences). It must match the whole string (anchored at both ends), for example `fd.name regex '[a-z]*/proc/[0-9]+/cmdline'`. It can be considerably slower than simple operators, so prefer the others when they suffice.
- `pmatch`: path prefix match, covered in its own skill.

Gotcha: for list-valued fields use `in` or `intersects`, not `=`. Syscall conditions conventionally start with an `evt.type` expression, since rules usually target one syscall type at a time.

## Checked

2026-11-08. Read the cited conditions page in full against the skill. Corrected unsupported or wrong claims in the draft and kept only statements the page supports.

Method: documentation only; no commands were run.
