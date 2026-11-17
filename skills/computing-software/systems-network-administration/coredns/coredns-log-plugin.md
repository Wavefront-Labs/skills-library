---
id: computing-software.systems-network-administration.coredns.coredns-log-plugin
name: coredns-log-plugin
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, log, query-log, format, class]
level: practitioner
status: docs-checked
description: "Write query logs with log, choosing names, common or combined formats, custom placeholders and response classes."
sources:
  - https://coredns.io/plugins/log/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: record queries and parts of replies.

Plain `log` writes every query in Common Log Format to stdout. For busy servers logging costs performance. Enabling or disabling log affects only query logging; other CoreDNS output still appears.

```
log [NAMES...] [FORMAT] {
    class CLASSES...
}
```

- NAMES limits logging to those names.
- FORMAT defaults to Common Log Format; `{common}` is the shortcut and `{combined}` adds the query opcode `{>opcode}`.
- Custom formats can use request and response placeholders, for instance `{type}`, `{name}`, `{class}`, `{proto}` (tcp or udp), `{remote}` and `{local}` (IPv6 shown in brackets) and `{size}`.
- `class` filters by response class: `success`, `denial` (NXDOMAIN or nodata), `error` (SERVFAIL, NOTIMP, REFUSED and so on), or `all` (the default). Using all means everything is logged regardless of other classes listed.

Example logging only failures:

```
. {
    log . {combined} {
        class error
    }
}
```

Multiple `class` lines are OR-ed, so `class denial` plus `class success` equals `class denial success`.

Other placeholders: `{port}`, `{duration}`, `{rcode}`, `{rsize}`, `{>rflags}`, `{>bufsize}`, `{>do}`, `{>id}`, `{>opcode}`, and `{/LABEL}` for any metadata label (replaced by `-` if undefined). The log plugin itself publishes `{/log/class}` (success, denial) and `{/log/type}` (NODATA, NXDOMAIN, NOERROR).

JSON output is chosen process-wide with the command-line flag `-log-format=json`, not a Corefile directive; `text` is the default and the name and class filters work the same in both modes.

## Checked

2026-11-08. Checked in full against the log plugin README. Replaced an unsupported closing remark about errors; added the remaining placeholders, OR-ing of class lines, log metadata and the -log-format=json flag.

Method: documentation only; no commands were run.
