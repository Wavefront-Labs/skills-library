---
id: computing-software.cybersecurity-defensive.falco.rule-style-and-performance
name: rule-style-and-performance
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [style-guide, evt-type, no-evttype, trailing-evttype, rule-performance]
level: advanced
status: docs-checked
description: "Write fast Falco conditions: positive evt.type first, avoid mixed event types, order filters, and heed the no-evttype warnings."
sources:
  - https://falco.org/docs/concepts/rules/style-guide/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The style guide applies to Falco 0.36 and above. Suggested key order in a rule: `rule`, `desc`, `condition`, `output`, `priority`, `tags`, then others.

Naming: a rule name starts with an upper-case letter; macros and lists use lowercase_with_underscores, for example `kernel_module_load`. The `desc` should say what is detected and also advise how to tune for false positives.

Condition principles, for performance:
- Every upstream rule needs an `evt.type` filter, or Falco warns `no-evttype`: without it the rule runs on all event types, a significant penalty.
- Put the `evt.type` filter first, and make it positive. Falco buckets filters per `evt.type`, so `evt.type!=execve` or a negative match triggers the `trailing-evttype` warning, because the rule cannot be limited to specific events.
- Do not mix unrelated event types in one rule; only variants such as `evt.type in (open, openat, openat2)`.
- After `evt.type`, order positive filters so each eliminates the most events. The `container` macro is the exception, as it removes many events quickly.
- Place exclusionary statements last, for known noise, often from profiling, such as `and not container.image.repository in (known_drop_and_execute_containers)`.

Example shape: `open_write and container and fd.name endswith release_agent and ...`.

More performance and style rules from the guide:
- Prefer `startswith` or `endswith` over `contains`; keep expressions short.
- Use `or` only for positive filters, never combined with negation; negate a positive sub-expression with `and not` and avoid double negation.
- Use parentheses consistently in nested conditions; extra ones do no harm.
- Upstream rules carry no `exceptions`, and upstream priority is at least `INFO`, never `DEBUG`. These are upstream-contribution rules, so local rules may differ.
- High-volume I/O syscalls can raise CPU use and cause kernel-side drops; upstream ships no I/O syscall rules enabled by default.

Gotcha: by default rules for one event type are matched "first match wins". Since Falco 0.36.0 `rule_matching: all` stops same-event-type rules overriding each other, at the cost of more CPU.

## Checked

2026-11-08. Read the Style Guide page in full. Removed an unsupported -V gotcha; added the remaining performance rules, upstream-only constraints and rule_matching: all.

Method: documentation only; no commands were run.
