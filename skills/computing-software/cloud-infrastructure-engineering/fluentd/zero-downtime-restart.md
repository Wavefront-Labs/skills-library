---
id: computing-software.cloud-infrastructure-engineering.fluentd.zero-downtime-restart
name: zero-downtime-restart
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, zero-downtime-restart, sigusr2, shared-socket, in-udp, in-tcp, in-syslog]
level: advanced
status: docs-checked
description: "Restart Fluentd completely without input downtime for in_udp, in_tcp and in_syslog using SIGUSR2 or RPC; the step-by-step mechanism."
sources:
  - https://docs.fluentd.org/deployment/zero-downtime-restart
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fluentd zero-downtime restart
A full restart where supported inputs keep receiving. Supported standard inputs (all v1.18.0): `in_udp`, `in_tcp`, `in_syslog`. Useful when clients cannot resend. Trigger with `SIGUSR2` on the supervisor or `/api/processes.zeroDowntimeRestart` (see `signals-and-process-model`, `http-rpc-endpoints`). Not available on Windows.

Mechanism:
1. Receive `SIGUSR2`.
2. Spawn a new supervisor.
3. Take over shared sockets.
4. Launch new workers in Source Only Mode, further limited to plugins that support this feature; received data goes to the temporary buffer. Meanwhile send `SIGTERM` to the old supervisor after a 10s delay.
5. The old supervisor stops and sends `SIGWINCH` to the new one.
6. New workers start fully and load the temporary buffer.

Plugin authors: implement `zero_downtime_restart_ready?`.

## Checked

2026-11-04. Confirmed against the Fluentd Zero-downtime restart page (docs.fluentd.org/deployment/zero-downtime-restart): supported inputs and v1.18.0, SIGUSR2 and RPC, the mechanism steps, zero_downtime_restart_ready?. The Windows exclusion comes from the RPC page (docs.fluentd.org/deployment/rpc). Nothing removed.

Method: documentation only; no commands were run.
