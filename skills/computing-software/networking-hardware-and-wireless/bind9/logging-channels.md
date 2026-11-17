---
id: computing-software.networking-hardware-and-wireless.bind9.logging-channels
name: logging-channels
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, logging, channel, syslog]
level: practitioner
status: docs-checked
description: "Define BIND 9 logging channels: file with versions and size, syslog, stderr, null, severity and print options."
sources:
  - https://bind9.readthedocs.io/en/latest/reference.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# logging channels
A `logging` block defines `channel` destinations and maps categories to them.

Channel destinations: `file` (with `versions`, `size`, `suffix increment|timestamp`), `syslog`, `stderr` or `null`. Channel options: `severity` (including `debug` with a level), `print-time`, `print-category`, `print-severity`, `buffered`.

```
logging {
    channel app_log {
        file "named.log" versions 3 size 20m;
        severity info;
        print-time yes;
    };
    category default { app_log; };
};
```

The default is `category default { default_syslog; default_debug; }`. Starting named with `-L` logs to the specified file instead of syslog: a fifth channel, `default_logfile`, is added and `category default { default_logfile; default_debug; }` applies. After renaming a log file for rotation, run `rndc closelogs`.

## Checked

2026-11-04. Confirmed against the ARM logging block, `channel`, `file`, `null` and predefined channel entries. Corrected the `-L` description.

Method: documentation only; no commands were run.
