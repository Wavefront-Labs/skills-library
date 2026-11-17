---
id: computing-software.cloud-infrastructure-engineering.fluent-bit.grep-filter
name: grep-filter
category: computing-software
field: cloud-infrastructure-engineering
product: fluent-bit
tags: [fluent-bit, grep-filter, regex, exclude, logical-op, record-accessor]
level: practitioner
status: docs-checked
description: "Keep or drop records by regular expression with the grep filter, including logical_op and nested keys."
sources: ["https://docs.fluentbit.io/manual/pipeline/filters/grep"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Grep filter

The `grep` filter keeps or excludes records by regular expression on a key's value.

| Key | Format | Meaning |
| --- | --- | --- |
| `regex` | `KEY REGEX` | keep records where `KEY` matches |
| `exclude` | `KEY REGEX` | drop records where `KEY` matches |
| `logical_op` | `AND`, `OR`, `legacy` | how several rules combine; default `legacy` |

In `legacy` mode the behaviour is `AND` when the filter is including and `OR` when it is excluding.

`KEY` accepts the record accessor syntax, so you can match nested values.

```yaml
pipeline:
  inputs:
    - name: tail
      path: lines.txt
      parser: json
  filters:
    - name: grep
      match: '*'
      regex: log aa
  outputs:
    - name: stdout
      match: '*'
```

This passes only records whose `log` value starts with `aa`.

Command-line equivalent:

```shell
fluent-bit -i tail -p 'path=lines.txt' -F grep -p 'regex=log aa' -m '*' -o stdout
```

Quote regular expressions carefully on the command line; a configuration file is easier.

To combine several `regex` or `exclude` rules, use `logical_op` (available from 2.1 or higher); with `logical_op` set, giving both `regex` and `exclude` is an error. In `legacy` mode, `exclude` rules must come first and there can be only one `regex`.

## Checked

2026-11-03. Confirmed on the Fluent Bit Grep filter page: regex, exclude and logical_op keys and defaults, legacy semantics, record accessor, the `log aa` example, and multiple-condition rules. Removed: an invented health-check use case and verification step.

Method: documentation only; no commands were run.
