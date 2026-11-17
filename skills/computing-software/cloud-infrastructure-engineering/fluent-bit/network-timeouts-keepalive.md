---
id: computing-software.cloud-infrastructure-engineering.fluent-bit.network-timeouts-keepalive
name: network-timeouts-keepalive
category: computing-software
field: cloud-infrastructure-engineering
product: fluent-bit
tags: [fluent-bit, networking, connect-timeout, keepalive, io-timeout, net-properties]
level: practitioner
status: docs-checked
description: "Set connect timeout, idle timeout and keepalive recycling for any Fluent Bit plugin that uses TCP."
sources: ["https://docs.fluentbit.io/manual/administration/networking"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Network timeouts and keepalive

Plugins that do network I/O share a common set of `net.*` properties. Put them in the input or output section.

| Property | Default | Meaning |
| --- | --- | --- |
| `net.connect_timeout` | `10s` | maximum time to establish a connection, including the TLS handshake |
| `net.connect_timeout_log_error` | `true` | log timeouts as errors; when off they are debug messages |
| `net.io_timeout` | `0s` | maximum time a connection can stay idle while assigned |
| `net.keepalive` | `true` | keep TCP connections open for reuse |
| `net.keepalive_idle_timeout` | `30s` | maximum idle time of a keepalive connection |
| `net.keepalive_max_recycle` | `2000` | times a keepalive connection can be used before it is retired |

Keepalive improves performance because communication channels are established beforehand; it applies to any component on TCP, including HTTP and TLS. Unused connections can be removed, and `net.keepalive_idle_timeout` controls how long one may sit idle.

```yaml
pipeline:
  outputs:
    - name: tcp
      match: '*'
      host: 127.0.0.1
      port: 9090
      format: json_lines
      net.connect_timeout: 5s
      net.keepalive: true
      net.keepalive_idle_timeout: 10s
```

DNS resolution, a slow network or incomplete TLS handshakes can delay or stall a new connection; `net.connect_timeout` bounds that wait, and the handshake counts against it.

To try it, run `nc -l 9090` on the receiving side and watch records arrive. With `net.keepalive` off, Fluent Bit closes the TCP connection after sending and netcat quits; with it on, the idle connection closes after `net.keepalive_idle_timeout`.

## Checked

Method: docs-checked 2026-11-09 against the Fluent Bit docs networking page (raw markdown, read in full).
