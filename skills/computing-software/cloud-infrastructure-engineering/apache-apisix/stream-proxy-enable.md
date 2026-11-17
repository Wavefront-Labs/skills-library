---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.stream-proxy-enable
name: stream-proxy-enable
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, stream-proxy, tcp, udp, proxy-mode, l4]
level: practitioner
status: docs-checked
description: "Enable APISIX layer-4 proxying: proxy_mode http&stream, stream_proxy tcp and udp listen entries, and the rule that stream routes need stream_proxy defined."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/stream-proxy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enable stream proxy

In `conf/config.yaml`:

```yaml
apisix:
  proxy_mode: http&stream        # or "stream" for stream only
  stream_proxy:
    tcp:
      - 9100                     # all interfaces
      - "127.0.0.1:9101"
    udp:
      - 9200
      - "127.0.0.1:9211"
```

Stream routes are rejected unless `stream_proxy` is defined.

Enable TLS on a TCP listen port:

```yaml
apisix:
  proxy_mode: http&stream
  stream_proxy:
    tcp:
      - addr: 9100
        tls: true
```

Certificates for TLS-over-TCP are configured per SNI through the Admin API SSL resource.

## Checked

2026-11-04: read the Stream Proxy page; proxy_mode values stream and http&stream, the stream_proxy tcp and udp listen entries, the stream-mode-disabled rule for stream routes, and the tls: true listen entry match. Nothing removed.

Method: documentation only; no commands were run.
