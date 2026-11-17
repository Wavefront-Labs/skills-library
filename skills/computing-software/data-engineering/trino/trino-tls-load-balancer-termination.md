---
id: computing-software.data-engineering.trino.trino-tls-load-balancer-termination
name: trino-tls-load-balancer-termination
category: computing-software
field: data-engineering
product: trino
tags: [tls, https, load-balancer, process-forwarded, tls-ciphers]
level: practitioner
status: docs-checked
description: "Put TLS in front of Trino at a load balancer with http-server.process-forwarded, and know the supported TLS versions and cipher settings."
sources: ["https://github.com/trinodb/trino/blob/master/docs/src/main/sphinx/security/tls.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Trino tls load balancer termination

All Trino authentication methods need TLS as the foundation, and by default Trino runs unsecured. The docs describe two approaches; terminating TLS at a load balancer or proxy is simplest and strongly preferred.

Load balancer approach: the balancer holds a valid, globally trusted certificate, accepts TLS and forwards to the coordinator, which typically keeps default HTTP on port 8080. The balancer adds a forwarded header such as `X-Forwarded-Proto: https`, telling the coordinator to treat the connection as already secured, so `http-server.https.enabled=true` is not needed. You must however set this in `config.properties`:

```text
http-server.process-forwarded=true
```

Clients then use the URL the load balancer exposes.

Supported standards when Trino terminates TLS itself: TLS 1.2 and TLS 1.3; TLS 1.1, 1.0 and all SSL are rejected. Trino defers to the JVM's default cipher suites and by default excludes older suites lacking forward secrecy using regex exclusions. To choose ciphers, set `http-server.https.included-cipher` to a comma-separated preference list, and if any is non-forward-secret also set `http-server.https.excluded-cipher=` to an empty value:

```text
http-server.https.included-cipher=TLS_RSA_WITH_AES_128_CBC_SHA,TLS_RSA_WITH_AES_128_CBC_SHA256
http-server.https.excluded-cipher=
```

Change ciphers only with your security managers; it may need a different SunJCE package and some locales restrict ciphers. Watch coordinator CPU after enabling HTTPS directly, since Java prefers CPU-heavy suites from a big list.

## Checked

2026-11-04. Read against the Trino docs page `security/tls.md` (GitHub source of the public docs): property names, defaults, allowed values, error messages, examples and behaviour described above match it. Nothing needed removing.
Method: documentation only; no commands were run.
