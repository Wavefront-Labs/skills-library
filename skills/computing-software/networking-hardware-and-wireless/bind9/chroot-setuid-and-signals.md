---
id: computing-software.networking-hardware-and-wireless.bind9.chroot-setuid-and-signals
name: chroot-setuid-and-signals
category: computing-software
field: networking-hardware-and-wireless
product: bind9
tags: [networking-hardware-and-wireless, bind9, chroot, setuid, signals]
level: advanced
status: docs-checked
description: "Run BIND 9 named in a chroot with -t and as an unprivileged user with -u, and control it with SIGHUP, SIGUSR1 and SIGTERM."
sources:
  - https://bind9.readthedocs.io/en/latest/chapter7.html
  - https://bind9.readthedocs.io/en/latest/chapter4.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# chroot setuid and signals
```
named -u 202 -t /path/to/chroot
```

`-t` runs named in a chroot sandbox and `-u` drops to an unprivileged user; the manual suggests running as an unprivileged user when using chroot. From named's view the chroot directory is the filesystem root, so `directory` and `pid-file` values must be relative to it. Depending on the OS you may need `/dev/zero`, `/dev/random`, `/dev/log` and `/etc/localtime` inside it.

Make files named writes to owned by that user before starting. An unprivileged named cannot bind new restricted ports after a reload.

Signals: SIGHUP reloads configuration and zones, SIGUSR1 closes the currently open log files, SIGTERM (and SIGINT) clean up and exit.

## Checked

2026-11-04. Confirmed against the ARM Chroot and Setuid section and the signals table in the Operations chapter: `-t`, `-u`, relative `directory` and `pid-file`, device and `/etc/localtime` locations, ownership of written files, restricted ports after reload, signal behaviour. Softened "use both together" and removed the claim that SIGUSR1 reopens logs.

Method: documentation only; no commands were run.
