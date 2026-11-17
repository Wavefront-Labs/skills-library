---
id: computing-software.networking-hardware-and-wireless.squid.access-log-modules
name: access-log-modules
category: computing-software
field: networking-hardware-and-wireless
product: squid
tags: [networking-hardware-and-wireless, squid, access-log, logging, daemon, syslog, acl-filtering]
level: practitioner
status: docs-checked
description: "Configure transaction logging with access_log: modules, format option, buffering, rotate and ACL filtering."
sources:
  - https://www.squid-cache.org/Doc/config/access_log/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# access_log
Syntax: `access_log <module>:<place> [option ...] [acl acl ...]`; disable with `access_log none [acl acl ...]`. It replaces `cache_access_log`.

Modules: `none`, `stdio` (write per request), `daemon` (helper, asynchronous), `syslog` (place facility.priority), `udp` and `tcp` (place `//host:port`).

Options: `logformat=name` (default `squid`), `buffer-size=64KB`, `on-error=die|drop`, `rotate=N` (stdio only; 0 disables renaming).

Only requests matching all listed ACLs are logged. The first ACL name should not contain `=` or match a logformat name; starting with `all` avoids that.

Default: `access_log daemon:/usr/local/squid/var/logs/access.log squid`.

## Checked

2026-11-04. Read the access_log directive page and confirmed the syntax, the cache_access_log replacement, the modules and place formats, the logformat, buffer-size, on-error and rotate options, the first-ACL-name note and the default. Nothing was removed.

Method: documentation only; no commands were run.
