---
id: computing-software.systems-network-administration.pi-hole.ftl-signals-and-reloads
name: ftl-signals-and-reloads
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [ftl-signals, sighup, realtime-signal]
level: advanced
status: docs-checked
description: "Choose the right signal for pihole-FTL: SIGHUP, real-time signal 0, RT 5 ARP refresh, SIGUSR1 cache dump and SIGUSR2 log reopen."
sources: ["https://docs.pi-hole.net/ftldns/signals/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Signals for pihole-FTL

**SIGHUP** is the big gun. It clears the entire DNS cache, re-reads `/etc/hosts`, `/etc/ethers` and dnsmasq host files, re-opens the FTL and gravity databases, re-reads privacy level, blocking status and `debug.*` settings, and recompiles all regex filters. No other dnsmasq config files are re-read.

**Real-time signals** are the scalpel. Their number varies by system, so check:

```bash
pihole-FTL sigrtmin
```

Assuming RTMIN is 35, send real-time signal 0 with `sudo pkill -SIG35 pihole-FTL`.

| Signal | Effect |
| --- | --- |
| RT 0 (35) | Re-open gravity.db, update blocked count, recompile regexes, clear the blocking cache, re-read privacy level; the DNS cache is not flushed. Preferred after manual `gravity.db` edits |
| RT 3 (38) | Reimport alias-clients and recompute their stats |
| RT 4 (39) | Re-resolve all client and upstream hostnames |
| RT 5 (40) | Re-parse the ARP/neighbour cache now |
| RT 1, 2, 6 | Reserved; do not use |
| RT 7 | Debug scan for hash collisions; can stall low-end devices |

**dnsmasq signals**

- `SIGUSR1` writes cache statistics and dumps the cache: `sudo killall -USR1 pihole-FTL`.
- `SIGUSR2` closes and reopens the log file when logging directly to a file, as used by logrotate.

**Checklist**

1. Use RT 0 after editing gravity.db (the page calls it the preferred signal for that).
2. Use SIGHUP only when you need the DNS cache flushed and the host files re-read.

## Checked

2026-11-03. Read the FTL Signals page: the SIGHUP list, the real-time signal table (RT 0 to 7), `pihole-FTL sigrtmin`, the `pkill -SIG35` example, and the SIGUSR1 and SIGUSR2 sections. Removed the `pihole reloadlists` checklist item (that command is not on the signals page) and the unsupported advice about when to use SIGHUP.

Method: documentation only; no commands were run.
