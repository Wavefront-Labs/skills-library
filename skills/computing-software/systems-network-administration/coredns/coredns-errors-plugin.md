---
id: computing-software.systems-network-administration.coredns.coredns-errors-plugin
name: coredns-errors-plugin
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, errors, logging, consolidate, stacktrace]
level: practitioner
status: docs-checked
description: "Log query processing errors to stdout and consolidate repetitive errors with regex, duration, level and show_first."
sources:
  - https://coredns.io/plugins/errors/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep error logs readable under load.

Basic form: `errors`. Errors seen during query processing go to standard output. The plugin can be used once per server block.

```
errors {
    stacktrace
    consolidate DURATION REGEXP [LEVEL] [show_first]
}
```

- `stacktrace` logs a stack trace during panic recovery.
- `consolidate` collects errors matching REGEXP (maximum 10000 characters) during DURATION from the first one, then prints one summary like `2 errors like '^read udp .* i/o timeout$' occurred in last 30s`. LEVEL is warning, error, info or debug.
- `show_first` logs the first error immediately and consolidates the rest. If only one error occurred no summary prints; with several, a summary shows the total.
- Several consolidate options with different durations and regexes may be used. An error matching several regexes is tied to the first.
- For performance, anchor patterns with `^` or `$`, e.g. `^failed to .*` or `.* timeout$`.

Example:

```
. {
    forward . 8.8.8.8
    errors {
        consolidate 5m ".* i/o timeout$" warning
        consolidate 30s "^Failed to .+"
    }
}
```

## Checked

2026-11-03. Page read: https://coredns.io/plugins/errors/ (the CoreDNS plugin page).

Confirmed: the syntax, options, defaults, limits, metric names and examples stated in this skill.

Removed or corrected: the debug-plugin remark (not on the errors page).

Method: documentation only; no commands were run.
