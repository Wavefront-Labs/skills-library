---
id: computing-software.cloud-infrastructure-engineering.vector.hardening-data-and-network
name: hardening-data-and-network
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [hardening, security, encryption, tls, swap, core-dumps, redact, vector]
level: advanced
status: docs-checked
description: "Secure Vector's data at rest and in transit and its network exposure."
sources:
  - https://vector.dev/docs/setup/going-to-prod/hardening/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Vector writes events to disk only if you configure disk buffers or swap is enabled. For data at rest:

- Enable whole disk encryption at the OS or file system level.
- Disable swap, to keep memory contents off disk (also faster). Give Vector enough memory.
- Restrict the data directory (such as `/var/lib/vector`) to the unprivileged Vector service account.
- Encrypt external storage such as archives, typically with server-side encryption.

For data in transit and in memory:

- Redact sensitive attributes such as PII, for example with the VRL `redact` function.
- Disable core dumps, since someone who can force one could read in-flight data. On Linux set `RLIMIT_CORE` to 0; `LimitCORE=0` in the systemd unit does this and is set automatically when installing through apt or yum.

Network:

- Use end-to-end TLS on all sources and sinks, even internal traffic.
- Use modern algorithms, for example TLS 1.3 where supported.
- Use a software or hardware firewall to allow only subnets Vector needs.

```ini
[Service]
LimitCORE=0
```

The docs frame this as an onion: data, process, host, network. Vector's Rust affine type system limits how long data stays in memory.

## Checked

Method: docs-checked 2026-11-09 against the full Vector hardening page (raw markdown from the vectordotdev/vector repo). Dropped an unsourced verification line.
