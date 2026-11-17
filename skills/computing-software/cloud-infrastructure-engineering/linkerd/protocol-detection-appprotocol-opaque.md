---
id: computing-software.cloud-infrastructure-engineering.linkerd.protocol-detection-appprotocol-opaque
name: protocol-detection-appprotocol-opaque
category: computing-software
field: cloud-infrastructure-engineering
product: linkerd
tags: [linkerd, protocol-detection, opaque-ports, appprotocol]
level: advanced
status: docs-checked
description: "Skip the 10-second protocol detection wait by declaring Service port protocols with appProtocol or opaque ports annotations."
sources:
  - https://linkerd.io/2.19/features/protocol-detection/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Linkerd detects whether a connection is HTTP by waiting up to 10 seconds for client bytes. If it cannot decide, it proxies as plain TCP, so HTTPRoute policy is not applied. Symptoms are proxy log lines such as `protocol detection timed out after 10s` or 10-second connection delays. Typical causes are protocols where the server speaks first (SMTP) or clients that connect without sending (Memcache). Traffic where the app itself does TLS is treated as opaque.

Declare the protocol on the Service port with `appProtocol` to skip detection:

- `linkerd.io/opaque` or `linkerd.io/tcp`: opaque TCP
- `http`: HTTP/1
- `kubernetes.io/h2c`: HTTP/2
- any other value: opaque TCP
- unset: automatic detection

Use the `config.linkerd.io/opaque-ports` annotation instead when `appProtocol` is not seen:

- pods receiving traffic from unmeshed clients, which cannot read the Service
- headless Services or direct pod connections

```yaml
annotations:
  config.linkerd.io/opaque-ports: "25,587,3306"
```

Multiple ports are a comma-delimited string, and the value replaces the default list rather than adding to it. The defaults include SMTP, MySQL, PostgreSQL, Redis, ElasticSearch and Memcache ports. NATS and MySQL Galera ports 4567 and 4568 are not in the default list and need configuration.

## Checked

2026-11-08. Confirmed against: https://linkerd.io/2.19/features/protocol-detection/. 10-second detection wait, opaque fallback and the HTTPRoute consequence, symptoms and causes, app-initiated TLS, the appProtocol table, the opaque-ports annotation cases, replace-not-augment rule, default port list and the NATS and Galera exceptions.

Removed or reworded: Nothing.

Method: documentation only; no commands were run.
