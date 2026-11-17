---
id: computing-software.systems-network-administration.openldap.slapd-command-line-options
name: slapd-command-line-options
category: computing-software
field: systems-network-administration
product: openldap
tags: [systems-network-administration, openldap, command-line, debug-levels, stopping-slapd, slapd-flags, chroot]
level: practitioner
status: docs-checked
description: "Start and stop OpenLDAP slapd with the right flags: -f, -F, -h, -u, -g, -r, -d, -l, -n, debug levels, foreground behaviour and clean shutdown."
sources:
  - https://www.openldap.org/doc/admin26/runningslapd.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# slapd command line options
Start: `/usr/local/libexec/slapd [options]`. Unless you give a debug level (even 0), slapd forks into the background.

- `-f <file>`: config file (default `/usr/local/etc/openldap/slapd.conf`).
- `-F <dir>`: config directory (default `/usr/local/etc/openldap/slapd.d`). With both `-f` and `-F`, the file is converted into the directory. With neither, the default directory is tried before the default file.
- `-h <URLs>`: listeners (default `ldap:///`).
- `-n <name>`: service name for logging (default `slapd`).
- `-l <LOCAL0-7>`: syslog facility (default LOCAL4).
- `-u user`, `-g group`: run as this user/group (name or numeric).
- `-r <dir>`: chroot after listeners open but before config is read.
- `-d <level>|?`: debug level; `?` prints the levels. Values add: `-d 1 -d 64` equals `-d 65`; `-1` is everything.

Debug levels: 1 trace, 2 packets, 4 args, 8 conns, 16 BER, 32 filter, 64 config, 128 ACL, 256 stats, 512 stats2, 1024 shell, 2048 parse, 16384 sync, 32768 none.

Stop cleanly:
```
kill -INT `cat /usr/local/var/slapd.pid`
```
A harder kill can lose data or corrupt the database.

## Checked

2026-11-09. Confirmed against the OpenLDAP 2.6 Admin Guide chapter 7 (-f, -F and their default paths, conversion and default-directory behaviour, -h default, -n, -l and LOCAL4, -u and -g, -r chroot timing, -d levels table and additive use, forking unless a debug level is given, kill -INT). Removed the verify line, which is not on this page.

Method: documentation only; no commands were run.

