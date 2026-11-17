---
id: computing-software.cloud-infrastructure-engineering.fluent-bit.network-connection-limits
name: network-connection-limits
category: computing-software
field: cloud-infrastructure-engineering
product: fluent-bit
tags: [fluent-bit, networking, max-worker-connections, net-backlog, tcp-keepalive, listener]
level: advanced
status: docs-checked
description: "Cap outbound connections per output worker and tune the listener backlog and TCP keepalive probes."
sources: ["https://docs.fluentbit.io/manual/administration/networking"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Connection limits and probes

**Outbound cap.** `net.max_worker_connections` in an output section (default `0`) sets the maximum number of TCP connections per worker. With five workers and a value of 10, at most 50 connections are allowed. When the limit is reached the output issues a retry. By default Fluent Bit creates connections on demand and keeps them alive; use the cap in highly scalable environments where you need to limit how many are created in parallel.

**Listener backlog.** For listening inputs such as HTTP, TCP, OpenTelemetry, Forward and Syslog, the operating system keeps a queue of pending connections. `net.backlog` (default `128`) sets how many can queue before new attempts are refused; raising it helps with bursts of incoming connections. On Linux the effective value can be capped by the kernel parameter `net.core.somaxconn`, which you can increase if you need more pending connections.

**TCP keepalive probes.** Socket-level settings, separate from `net.keepalive`:

| Property | Default | Meaning |
| --- | --- | --- |
| `net.tcp_keepalive` | `off` | enable TCP keepalive |
| `net.tcp_keepalive_time` | `-1` | interval between the last data packet sent and the first probe |
| `net.tcp_keepalive_interval` | `-1` | interval between probes when no response is received |
| `net.tcp_keepalive_probes` | `-1` | unacknowledged probes before the connection is considered dead |

```yaml
pipeline:
  outputs:
    - name: http
      match: '*'
      host: 192.168.5.6
      port: 8080
      workers: 5
      net.max_worker_connections: 10
      net.tcp_keepalive: on
```

Worker counts are covered in `computing-software.cloud-infrastructure-engineering.fluent-bit.output-workers`.

## Checked

Method: docs-checked 2026-11-09 against the Fluent Bit docs networking page and multithreading page (raw markdown, read in full).
