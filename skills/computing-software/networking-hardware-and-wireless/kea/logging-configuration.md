---
id: computing-software.networking-hardware-and-wireless.kea.logging-configuration
name: logging-configuration
category: computing-software
field: networking-hardware-and-wireless
product: kea
tags: [networking-hardware-and-wireless, kea, logging, loggers, output-options, debuglevel, log-rotation]
level: practitioner
status: docs-checked
description: "Configure Kea loggers: names, severity, debuglevel, output-options (file, stdout, syslog), rotation with maxsize and maxver, and debug level meanings."
sources:
  - https://kea.readthedocs.io/en/latest/arm/logging.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kea logging configuration
With no loggers configured, Kea logs INFO or above to stdout. Each entry in `loggers` has:
- `name`: e.g. `kea-dhcp4`; children such as `kea-dhcp4.alloc-engine` inherit from the root logger.
- `severity`: FATAL, ERROR, WARN, INFO, DEBUG or NONE.
- `debuglevel`: 0 (least verbose) to 99, used only with DEBUG. It is inherited from the root logger only if severity is also omitted; an entry with explicit DEBUG severity and no debuglevel defaults to 0 and logs no debug messages, so set both together.
- `output-options`: list of destinations.

```json
"loggers": [ { "name": "kea-dhcp4", "severity": "INFO",
  "output-options": [ { "output": "kea-dhcp4.log",
    "maxsize": 2048000, "maxver": 4 } ] } ]
```

Output options: `output` (stdout, stderr, syslog, `syslog:name`, or a file name; since Kea 2.7.9 files must be in the compiled log directory, overridable with `KEA_LOG_FILE_DIR`, so give a bare file name), `flush` (boolean, default true), `maxsize` (bytes, default 10240000; any value below 204800, including 0, disables rotation), `maxver` (default and minimum 1; at most the active file plus maxver rotated files are kept) and `pattern`. The key `output_options` is deprecated since 2.7.4; use `output-options`.

Debug levels: 0 startup/shutdown, 10 API commands, 15 drop reasons, 40 tracing, 45 more detail, 50 expression evaluations, hook point status, lease and packet processing details, 55 all details including full packet contents.

Startup environment variables (used before the configuration is read): `KEA_LOCKFILE_DIR` (lock file directory; the value `none` disables the lock file), `KEA_LOGGER_DESTINATION` (stdout, stderr, `syslog[:fac]` or a file name).

If keactrl starts the servers in verbose mode (`kea_verbose` set to yes), the configured severity has no effect and DEBUG is used.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Kea ARM logging chapter (19.1.1 loggers, severity, debuglevel, output-options sections, 19.1.3 startup variables, 19.2 logging levels). Changed the sample output path to a bare file name because of the 2.7.9 path restriction, and added the debuglevel inheritance rule and the keactrl verbose note from the page.
