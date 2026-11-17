---
id: computing-software.systems-network-administration.openldap.loglevel-configuration
name: loglevel-configuration
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, loglevel, olcloglevel, syslog, debugging, acl-debug]
level: practitioner
status: docs-checked
description: "Set the OpenLDAP slapd log level with integers, hex or keywords (stats, acl, sync, conns, filter), understand the none and 0 difference, and defaults."
sources:
  - https://www.openldap.org/doc/admin26/slapdconfig.html
  - https://www.openldap.org/doc/admin26/slapdconf2.html
  - https://www.openldap.org/doc/admin26/tuning.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# loglevel configuration
`loglevel` (slapd.conf) or `olcLogLevel` (cn=config) selects what goes to syslog (LOG_LOCAL4 by default). Values are additive and may be decimal, hex, a list, or keywords. These are equivalent: `loglevel 129`, `loglevel 0x81`, `loglevel 128 1`, `loglevel acl trace`.

Levels: 1 trace, 8 conns, 32 filter, 64 config, 128 ACL, 256 stats, 512 stats2, 16384 sync, 32768 none, -1 any (everything), 0 nothing.

Examples:
```
loglevel -1
loglevel conns filter
loglevel none
```
In cn=config: `olcLogLevel: Stats` (LDIF) or `olcLogLevel conns filter`.

Facts:
- Default is `stats`.
- `none` logs only messages that are always logged; `0` logs nothing. Keep the default in production, because `loglevel 0` makes it hard to see when problems start.
- Debug levels other than the stats ones need a build with `--enable-debug` (the default).
- For deep debugging, run `slapd -d <level>` and capture stderr rather than syslog, which can drop messages under load.

## Checked

2026-11-04. Confirmed against the Administrator's Guide slapd.conf and slapd.d chapters and Tuning chapter: loglevel and olcLogLevel, additive integer, hex, list and keyword forms with the 129, 0x81, 128 1, acl trace equivalence, the level table (1 trace, 8 conns, 32 filter, 64 config, 128 ACL, 256 stats, 512 stats2, 16384 sync, 32768 none, -1 any), none versus 0, default stats, --enable-debug requirement, LOG_LOCAL4, debug flag with stderr rather than lossy syslog, loglevel 0 not ideal in production. Removed the slapacl remark and the conn=/op= verify line, which those pages do not state.

Method: documentation only; no commands were run.
