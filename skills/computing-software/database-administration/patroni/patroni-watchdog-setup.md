---
id: computing-software.database-administration.patroni.patroni-watchdog-setup
name: patroni-watchdog-setup
category: computing-software
field: database-administration
product: patroni
tags: [patroni, watchdog, split-brain, softdog, linux]
level: practitioner
status: docs-checked
description: "Why Patroni uses a watchdog and how to enable the Linux software watchdog."
sources:
  - https://patroni.readthedocs.io/en/latest/watchdog.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: add a second split-brain safeguard.

Patroni normally stops PostgreSQL when the leader lock update fails. That can fail if Patroni crashes (bug, out-of-memory, accidental kill), shutdown is too slow, or Patroni cannot run due to high load or a paused VM. A watchdog device resets the whole system when it gets no keepalive in time.

Behaviour:
- Patroni tries to activate the watchdog before promoting PostgreSQL. If activation fails and watchdog mode is required, the node refuses to become leader. It also checks whether the watchdog configuration allows leadership when deciding to join an election.
- After demotion (for example manual failover) the watchdog is disabled again, and it is disabled in paused state.
- Only the Linux watchdog device interface is supported.

Default configuration tries to use `/dev/watchdog` on Linux if Patroni can access it. For most use cases the software watchdog built into the Linux kernel is secure enough. Enable it as root before starting Patroni:

```
modprobe softdog
chown postgres /dev/watchdog
```

Replace `postgres` with the user Patroni runs under. For testing add `soft_noboot=1` to the modprobe command line so the watchdog only logs a line in the kernel ring buffer (visible via dmesg). Patroni logs information about the watchdog when it is enabled.

## Checked

2026-11-08. Confirmed against the Patroni watchdog support page (read in full). Removed the `watchdog:` YAML block (mode values, device, safety_margin keys), which belongs to the YAML configuration page that is not cited here.

Method: documentation only; no commands were run.
