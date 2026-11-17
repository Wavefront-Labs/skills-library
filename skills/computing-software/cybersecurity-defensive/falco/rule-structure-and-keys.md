---
id: computing-software.cybersecurity-defensive.falco.rule-structure-and-keys
name: rule-structure-and-keys
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [falco-rule, rule-keys, condition, skip-if-unknown-filter, source]
level: intro
status: docs-checked
description: "Write a Falco rule with the required rule, desc, condition, output and priority keys plus optional enabled, tags, warn_evttypes, skip-if-unknown-filter and source."
sources:
  - https://falco.org/docs/concepts/rules/basic-elements/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A Falco rule is a YAML object in a rules file. Required keys: `rule` (short unique name), `desc`, `condition` (a Boolean filter expression), `output` and `priority`.

```yaml
- rule: shell_in_container
  desc: notice shell activity within a container
  condition: >
    (evt.type in (execve, execveat)) and
    container.id != host and proc.name = bash
  output: >
    shell in a container | user=%user.name container_id=%container.id
    shell=%proc.name parent=%proc.pname cmdline=%proc.cmdline
  priority: WARNING
```

Optional keys:
- `exceptions`: cases that suppress the alert.
- `enabled`: default `true`; `false` means the rule is neither loaded nor matched.
- `tags`: a list of tags.
- `warn_evttypes`: default `true`; `false` suppresses warnings about a rule with no event type.
- `skip-if-unknown-filter`: default `false`. When `true`, a condition using a field unknown to this Falco version is silently accepted but never run. When `false`, Falco reports an error and exits.
- `source`: event source to evaluate, default `syscall`; others include `k8s_audit` or a source plugin name.

`priority` is case-insensitive and one of `emergency`, `alert`, `critical`, `error`, `warning`, `notice`, `informational`, `debug`. It is a severity, not an ordering: rule order is set by definition and load order. In `output`, fields are prefixed with `%`, a field not set for the event prints as `<NA>`, and transformers work there too, for example `%toupper(user.name)`.

Gotcha: a condition with no syscall clause only checks event metadata. `container.id != host and proc.name = bash` therefore fires for every syscall that bash makes. Add `evt.type in (execve, execveat)` to alert once per spawn.

## Checked

2026-11-08. Read the Basic Elements page in full. Added priority values and semantics and output interpolation notes.

Method: documentation only; no commands were run.
