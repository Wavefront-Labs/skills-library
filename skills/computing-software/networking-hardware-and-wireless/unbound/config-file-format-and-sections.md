---
id: computing-software.networking-hardware-and-wireless.unbound.config-file-format-and-sections
name: config-file-format-and-sections
category: computing-software
field: networking-hardware-and-wireless
product: unbound
tags: [networking-hardware-and-wireless, unbound, unbound-conf, section-clauses, syntax, config-file]
level: intro
status: docs-checked
description: "Read and write unbound.conf: keyword syntax, comments and the section clauses (server, remote-control, zones, view, rpz, module sections)."
sources:
  - https://unbound.docs.nlnetlabs.nl/en/latest/manpages/unbound.conf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# config file format and sections
Whitespace separates keywords and indentation is insignificant, though recommended. Comments start with `#` and run to end of line; empty lines are ignored. Keywords that end with a colon are either options or section clauses, and the file is divided into sections, each introduced by a section clause.

Recognised section clauses: `server:` (most options), `remote-control:`, `stub-zone:`, `forward-zone:`, `auth-zone:`, `view:`, `python:`, `dynlib:`, `dnscrypt:`, `cachedb:`, `dnstap:` and `rpz:` (needs the `respip` module).

Section clauses can be repeated anywhere in the file, including in included files, to group related options.

The manual's minimal example sets `directory`, `username: unbound`, `chroot` and `pidfile`, listens on `0.0.0.0` and `::0`, and allows `10.0.0.0/8` and `2001:db8::/64`; most settings stay at defaults. Start it with `unbound -c <config path>`. The source distribution ships an `example.conf` listing all options.

## Checked

2026-11-08. Read the File Format, Example, Section Clauses and Including Files text of the unbound.conf manual. Claims confirmed; description shortened.

Method: documentation only; no commands were run.
