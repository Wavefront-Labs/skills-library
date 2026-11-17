---
id: computing-software.cloud-infrastructure-engineering.fluentd.in-tail-unmatched-lines-and-faq
name: in-tail-unmatched-lines-and-faq
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, in-tail, emit-unmatched-lines, multiline, pattern-not-match, incomplete-line]
level: practitioner
status: docs-checked
description: "Diagnose in_tail warnings: pattern not match, got incomplete line before first line, a file not being read, and unreadable file messages."
sources:
  - https://docs.fluentd.org/input/tail
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# in_tail warnings and FAQ
- **`pattern not match`**: the `<parse>` type does not match the line (for example `@type json` and a CSV line). Set `emit_unmatched_lines true` to emit `{"unmatched_line": "<line>"}` instead of only warning.
- **`got incomplete line before first line`** (multiline parser with `format_firstline` only): lines before the first matching start line are dropped. Causes: reading begins mid-record (after rotation, or startup with `read_from_head false`, temporary and harmless); `format_firstline` does not match the real first line (warning repeats, fix the pattern); one `<parse>` applied to files of different formats via a glob (use separate sources). Because `emit_unmatched_lines` defaults to false the warning is the only sign data is dropped.
- **Not reading the file**: `in_tail` follows `tail -F` and reads only new lines; use `read_from_head true` for existing content.
- **`/path/to/file unreadable. It is excluded and would be examined next time`**: a permission problem; see `linux-capabilities-for-in-tail` and `ignore_repeated_permission_error`.
- Since v1.12.0 `in_tail` handles `CAP_DAC_READ_SEARCH` and `CAP_DAC_OVERRIDE` if Fluentd's Linux capability handling module is enabled.

A `<parse>` section is required; if its `@type` contains `multiline`, `in_tail` works in multiline mode. The `format` parameter is deprecated.

## Checked

2026-11-04. Confirmed against the Fluentd tail input page (docs.fluentd.org/input/tail), parameters and FAQ sections: pattern not match, emit_unmatched_lines default and record shape, incomplete-line warning causes, tail -F behaviour and read_from_head, unreadable-file message, v1.12.0 capabilities, required parse section, deprecated format. Added the capability-module condition from the page.

Method: documentation only; no commands were run.
