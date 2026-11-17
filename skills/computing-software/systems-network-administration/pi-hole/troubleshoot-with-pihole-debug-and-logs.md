---
id: computing-software.systems-network-administration.pi-hole.troubleshoot-with-pihole-debug-and-logs
name: troubleshoot-with-pihole-debug-and-logs
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [pihole-debug, pihole-tail, log-flush]
level: practitioner
status: draft
description: "Diagnose Pi-hole problems with the debugger, live log tail, log flush, logging toggle and list lookup."
sources: ["https://docs.pi-hole.net/main/pihole-command/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Debug and log commands

**Debugger.** `pihole debug` runs `/opt/pihole/piholeDebug.sh`. It attempts to diagnose issues and links to an FAQ describing how to fix them. When it finishes you may upload the generated log to the Pi-hole developers.

**Watch queries live**

```bash
pihole tail
```

Useful for a problematic site. The DNS query log is `/var/log/pihole/pihole.log`; FTL's own log is `/var/log/pihole/FTL.log`.

**Empty or rotate the log**

```bash
pihole flush
```

It also rotates the log daily if `logrotate` is installed.

**Turn query logging on or off**

```bash
pihole logging off
```

(`pihole logging --help` lists the options.) The equivalent setting is `dns.queryLogging`.

**Find which list blocks a domain**

```bash
pihole query -exact example.com
```

This searches allowlist, denylist, wildcards and subscribed lists, converting internationalised names to punycode first.

**Network table.** `pihole networkflush` empties the network table; add `--arp` to clear the ARP table too.

**Checklist**

1. Reproduce the problem while running `pihole tail`.
2. Run `pihole query` for the affected domain.
3. Run `pihole debug` if the cause is still unclear.
