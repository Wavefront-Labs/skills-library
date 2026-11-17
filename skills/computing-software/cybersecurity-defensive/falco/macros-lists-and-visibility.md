---
id: computing-software.cybersecurity-defensive.falco.macros-lists-and-visibility
name: macros-lists-and-visibility
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [falco-macro, falco-list, list-visibility, rule-reuse, load-order]
level: practitioner
status: docs-checked
description: "Define reusable Falco macros and lists, and obey the load-order visibility rules between lists, macros and rules."
sources:
  - https://falco.org/docs/concepts/rules/basic-elements/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Macros are named, reusable condition fragments; lists are named collections of values.

```yaml
- macro: container
  condition: (container.id != host)
- macro: spawned_process
  condition: (evt.type in (execve, execveat))
- list: shell_binaries
  items: [bash, csh, ksh, sh, tcsh, zsh, dash]
- macro: shell_procs
  condition: proc.name in (shell_binaries)
```

A rule can then say `spawned_process and container and shell_procs`.

Keys: a macro has `macro` and `condition`; a list has `list` (a unique slug name) and `items`. Referring to a list inserts its items in place. Lists cannot be parsed as filter expressions.

Visibility rules, which are load-order dependent:
- A list can only reference lists defined before it.
- A macro can only reference macros defined before it.
- A macro can reference any list, even one defined later.
- A rule can reference any macro, even one defined later.

The same load-order principle applies across multiple rules files, so the order of files decides how appending and overriding work.

Lists can include other previously defined lists (`items: [shell_binaries, userexec_binaries]`), and macros can include previously defined macros. Referring to a list inserts its items, as in `proc.name in (known_binaries)`.

Gotcha: default macros such as `container` and `spawned_process` ship in falco_rules.yaml, so reuse them rather than redefining.

## Checked

2026-11-08. Read the cited basic-elements page in full and corrected statements that went beyond it.

Method: documentation only; no commands were run.
