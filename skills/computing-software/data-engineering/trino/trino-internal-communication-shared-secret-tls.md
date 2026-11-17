---
id: computing-software.data-engineering.trino.trino-internal-communication-shared-secret-tls
name: trino-internal-communication-shared-secret-tls
category: computing-software
field: data-engineering
product: trino
tags: [internal-communication, shared-secret, internal-tls, https-required, secure-random-algorithm]
level: advanced
status: docs-checked
description: "Secure Trino node-to-node traffic with a shared secret and internal TLS, verify it with active workers, and understand the performance cost."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/security/internal-communication.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino internal communication shared secret tls

A shared secret is mandatory when any client authentication is used, and when internal TLS is enabled. Set the same value in `config.properties` on every node:

```text
internal-communication.shared-secret=<secret>
```

Use a large random key, for example `openssl rand 512 | base64 -w 0`.

Verify: start two or more nodes with the secret, open the Web UI and note `ACTIVE WORKERS`. Change the secret on one worker and restart it; the count should drop by one because the worker fails authentication and does not register. Revert the change, restart and confirm the count recovers.

Internal TLS (optional, extra layer). Configure every node identically, and still enable TLS directly on the coordinator for client access:
1. Shared secret as above.
2. `internal-communication.https.required=true` (automatic certificate creation and trust).
3. `discovery.uri=https://<coordinator ip address>:<https port>`. Hostnames and FQDNs are not supported; automatic certificates work only with IP addresses.
4. On all workers: `http-server.https.enabled=true` and `http-server.https.port=<https port>`.
5. Restart all nodes.

Performance: queries moving little data between nodes, such as `SELECT count(*)`, are barely affected. Distributed joins, aggregations and windows that repartition can slow by 10% to over 100%. Internal TLS uses HTTP/2 by default; turn off with `internal-communication.http2.enabled=false`.

Tuning: TLS entropy comes from `/dev/urandom`, which can bottleneck on very fast networks. Try `http-server.https.secure-random-algorithm=SHA1PRNG` on all nodes; it seeds from blocking `/dev/random`, so if entropy is short add `-Djava.security.egd=file:/dev/urandom` to `jvm.config`.

## Checked

2026-11-09. Pages read in full against this skill:
- https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/security/internal-communication.md

Confirmed (page read as raw markdown): when the shared secret is required, the verification steps, the internal TLS configuration steps, the IP-address-only limit, the performance figures and the SHA1PRNG tuning.
Removed or reworded: nothing; every concrete claim matched the page.

Method: documentation only; no commands were run.
