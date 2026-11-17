---
id: computing-software.networking-hardware-and-wireless.bind9.named-checkconf-and-checkzone
name: named-checkconf-and-checkzone
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, named-checkconf, named-checkzone, syntax-check]
level: practitioner
status: docs-checked
description: "Check BIND 9 configuration and zone files before loading: named-checkconf options -p -z -e, and named-checkzone options -d -i -f -F."
sources:
  - https://bind9.readthedocs.io/en/latest/manpages.html
  - https://bind9.readthedocs.io/en/latest/chapter4.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# named checkconf and checkzone
`named-checkconf [file]` checks the syntax, not the semantics, of `named.conf` and everything it includes (default `/etc/named.conf`). It does not read `rndc.conf` or `rndc.key`; run it on those explicitly.

Options: `-z` also load and check primary zone files, `-p` print the configuration in canonical form (with `-x` hiding secrets), `-e` print the effective configuration, `-b` print built-in defaults, `-l` list zones, `-k` check `dnssec-policy` keys against key files, `-a` skip the key algorithm check, `-j` read journals, `-c` core configuration only, `-i` ignore deprecation warnings, `-t dir` chroot.

`named-checkzone zone file` checks syntax and integrity of a zone file. Options: `-d` debug, `-q` quiet, `-j` read the journal, `-J file` journal path, `-c class`, `-C mode` (`check-svcb:fail` or `check-svcb:ignore`), `-f format` input format, `-F format` output format, `-i mode` post-load integrity checks (`full` default, `full-sibling`, `local`, `local-sibling`, `none`).

Do not run `named-checkzone` on untrusted zone text.

## Checked

2026-11-04. Read the named-checkconf and named-checkzone man pages: synopsis, every listed option, the -i modes, the -C modes and the untrusted-zone warning confirmed. Removed an unconfirmed run-before-reload instruction.

Method: documentation only; no commands were run.
