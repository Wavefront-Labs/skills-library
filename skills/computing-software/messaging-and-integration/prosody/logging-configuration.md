---
id: computing-software.messaging-and-integration.prosody.logging-configuration
name: logging-configuration
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, logging, syslog, log-levels, logrotate]
level: practitioner
status: docs-checked
description: "Prosody log option forms: a single file, a *sink such as *syslog or *console, and a level table; levels debug, info, warn, error; logrotate."
sources:
  - https://prosody.im/doc/logging
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Logging

Single file (logs info and higher by default):

```lua
log = "prosody.log"
```

Single sink, prefixed with `*` (`console` built in; `syslog` needs mod_posix loaded):

```lua
log = "*syslog"
```

Split by level:

```lua
log = {
    debug = "/var/log/prosody/prosody.log"; -- debug and higher
    error = "*syslog"; -- error and higher
}
```

Levels, lowest to highest: `debug` (most output, for diagnosis), `info` (routine events), `warn` (possible problems), `error` (investigate).

Prosody is compatible with tools like logrotate, which should work automatically for pre-built packages; for source installs the logging-for-packagers page has an example logrotate configuration.

## Checked

2026-11-04: confirmed against prosody.im/doc/logging (single file, sink prefix, split config, levels, logrotate). Removed the claim that `prosodyctl reload` reopens log files and a generic verify line, which the page does not state.
Method: documentation only; no commands were run.
