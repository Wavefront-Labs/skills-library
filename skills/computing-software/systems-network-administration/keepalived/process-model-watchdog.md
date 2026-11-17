---
id: computing-software.systems-network-administration.keepalived.process-model-watchdog
name: process-model-watchdog
category: computing-software
field: systems-network-administration
product: keepalived
tags: [systems-network-administration, keepalived, architecture, watchdog, process-model, vrrp-child, checker-child, scheduler]
level: practitioner
status: docs-checked
description: "Keepalived runs a parent watchdog plus a VRRP child and a healthcheck child, each with its own scheduler, restarted via hello packets sent every 5 seconds."
sources:
  - https://keepalived.readthedocs.io/en/latest/software_design.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Process model and watchdog

Keepalived is three processes: a minimal parent that acts as a watchdog, and two forked children, one for VRRP and one for healthchecking.

- Each child has its own I/O multiplexer (a central select loop). VRRP is more timing-sensitive than healthchecking, so it gets separate scheduling.
- The healthcheck child is kept minimal, with few foreign libraries, so its main loop stays nearly idle and avoids self-inflicted faults.

Watchdog mechanics:
- Each child opens a Unix domain socket and accepts connections.
- At bootstrap the parent connects to those sockets and sends a hello packet every 5 seconds.
- If the parent cannot send a hello, it restarts that child.
- Hello packets pass through the child's scheduler, so a deadlock in the child's loop is detected.
- On a broken pipe the parent uses SysV signals to test whether the child is alive and restarts it if needed.

Operational consequences: seeing parent plus two child processes in the process list is normal. Respawn of children is on by default and can be disabled with the dont-respawn command-line option.

## Checked

2026-11-04: process split, per-child scheduler, 5 s hello packets, unix domain sockets, sysV signal check confirmed against the Software Design page; respawn default and the dont-respawn option (-R) against the Programs synopsis. Removed the Verify line.
Method: documentation only; no commands were run.
