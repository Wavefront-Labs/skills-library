---
id: computing-software.cloud-infrastructure-engineering.netdata.streaming-tls
name: streaming-tls
category: computing-software
field: cloud-infrastructure-engineering
product: netdata
tags: [netdata, streaming-tls, ssl-destination, certificate-verification]
level: advanced
status: docs-checked
description: "Encrypt Child-to-Parent streaming with TLS by appending SSL to the destination in stream.conf, with the self-signed certificate caveat."
sources:
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/observability-centralization-points/metrics-centralization-points/configuration.md
  - https://raw.githubusercontent.com/netdata/netdata/master/docs/observability-centralization-points/metrics-centralization-points/faq.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
TLS is recommended but not required to get started. Streaming is Netdata's own binary TCP protocol, not HTTP; `:SSL` wraps it in TLS (it is not HTTPS). Streams are also compressed on top of TLS.

1. Parent: generate an SSL key and certificate with `openssl`, following "Securing Netdata Agents" in the docs, and enable TLS on the Parent's web server.
2. Child `stream.conf`:

```
[stream]
    enabled = yes
    destination = 203.0.113.0:SSL
    ssl skip certificate verification = yes
    api key = 11111111-2222-3333-4444-555555555555
```

3. Restart both Parent and Child.

The docs example uses self-signed certificates, which is why verification is skipped.

Gotchas:
- HTTP proxies cannot sit between Parent and Child, because streaming shares the web server port but is not HTTP.
- `stream.conf` contains sensitive keys and IPs.

Connection log messages are covered in the streaming-troubleshoot-logs skill.

## Checked

2026-11-04: TLS recommended but optional, the `:SSL` destination, `ssl skip certificate verification`, the example stream.conf, restarting both nodes, TLS not being HTTPS, compression on top of TLS, the HTTP proxy limitation and stream.conf sensitivity confirmed against the Netdata Configuring Metrics Centralization Points page and FAQ. Removed an unsourced CAfile/CApath claim and verify step.

Method: documentation only; no commands were run.
