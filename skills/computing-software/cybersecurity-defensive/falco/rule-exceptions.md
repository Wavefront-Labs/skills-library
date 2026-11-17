---
id: computing-software.cybersecurity-defensive.falco.rule-exceptions
name: rule-exceptions
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [exceptions, exception-fields, comps, values, false-positives]
level: practitioner
status: docs-checked
description: "Define Falco rule exceptions with fields, comps and values tuples, and understand the condition they expand into."
sources:
  - https://falco.org/docs/concepts/rules/exceptions/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rules have supported an optional `exceptions` key since Falco 0.28.0. Exceptions let a rule author declare which combinations of actor and target may be excluded, instead of piling `and not some_macro` clauses onto the condition.

```yaml
- rule: Write below binary dir
  condition: open_write and bin_dir
  exceptions:
   - name: proc_writer
     fields: [proc.name, fd.directory]
     comps: [=, =]
     values:
       - [my-custom-yum, /usr/bin]
       - [my-custom-apt, /usr/local/bin]
   - name: proc_filenames
     fields: [proc.name, fd.name]
     comps: [=, in]
     values:
       - [my-custom-dpkg, [/usr/bin, /bin]]
```

`name` is an arbitrary label; it only links values in a later override. `fields` extract values from events, `comps` are operators aligned one-to-one with the fields, and `values` is a list of tuples aligned with them. The `proc_writer` exception is equivalent to adding `and not ((proc.name=my-custom-yum and fd.directory=/usr/bin) or (proc.name=my-custom-apt and fd.directory=/usr/local/bin))`. When a comparison operator is `in`, the matching tuple item must be a list, so `proc_filenames` equals `and not (proc.name=my-custom-dpkg and fd.name in (/usr/bin, /bin))`.

Design point: exceptions belong to the rule so its author decides what counts as valid. An actor plus target (process and directory) is allowed; a process name alone would be too broad.

Gotcha: each values tuple must have the same length as `fields` and `comps`, with items aligned one-to-one. Be specific: include actor, action and target (for example `proc.name` plus `fd.directory`), and use `in` or `pmatch` with lists to group several process names or paths in one exception.

## Checked

2026-11-08. Read the cited exceptions page in full and corrected draft details to match the documented fields, comps and values semantics.

Method: documentation only; no commands were run.
