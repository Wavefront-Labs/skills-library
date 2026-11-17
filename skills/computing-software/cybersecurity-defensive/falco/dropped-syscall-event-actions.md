---
id: computing-software.cybersecurity-defensive.falco.dropped-syscall-event-actions
name: dropped-syscall-event-actions
category: computing-software
field: cybersecurity-defensive
product: falco
tags: [dropped-events, syscall-event-drops, ring-buffer, throttling, token-bucket]
level: practitioner
status: docs-checked
description: "Choose what Falco does on dropped syscall events: ignore, log, alert or exit, and why alert throttling is off by default."
sources:
  - https://falco.org/docs/concepts/event-sources/kernel/dropped-events/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
When at least one syscall event is dropped because the kernel buffer was full, Falco takes the configured actions:

- `ignore`: nothing happens. An empty list means ignore.
- `log`: logs a CRITICAL message noting the buffer was full.
- `alert`: emits a Falco alert that the buffer was full.
- `exit`: exits Falco with a non-zero return code.

Examples of what you see:
`Falco internal: syscall event drop. 1 system calls dropped in last second.`
with the alert form `Critical Falco internal: syscall event drop. 1 system calls dropped in last second.(n_drops=1 n_evts=1181)`. With `exit` Falco ends with `Exiting.`

The actions and the token-bucket throttling parameters are in the `syscall_event_drops` section of `falco.yaml`.

To limit floods of logs and alerts there is an alert throttling mechanism. It is disabled by default; before Falco 0.33.0 it was enabled by default. Enable it through the `outputs` entry of the configuration.

Pair this with the metrics counters (`scap.n_drops_perc`) and the troubleshooting pages for dropping, which cover buffer size and CPU load.

Falco reads the kernel's event counters every second (since v0.15.0); a drop is counted when the kernel tried to write to the shared buffer but found it full. Drops can leave Falco's view of processes, files, containers and orchestrator metadata incomplete, which can affect rules that depend on that metadata.

Gotcha: `exit` is the strictest choice; if you use it, something else (for example your service manager or orchestrator) has to restart Falco.

## Checked

2026-11-08. Read the cited dropped-events page in full and corrected details to match it.

Method: documentation only; no commands were run.
