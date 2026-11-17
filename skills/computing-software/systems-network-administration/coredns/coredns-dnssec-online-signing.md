---
id: computing-software.systems-network-administration.coredns.coredns-dnssec-online-signing
name: coredns-dnssec-online-signing
category: computing-software
field: systems-network-administration
product: coredns
tags: [coredns, dnssec, signing, nsec, ecdsa]
level: advanced
status: docs-checked
description: "Sign responses on the fly with the dnssec plugin using key files or AWS Secrets Manager, including CSK versus ZSK/KSK modes."
sources:
  - https://coredns.io/plugins/dnssec/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: serve DNSSEC-signed answers without a signed zone file.

Any reply that does not or cannot do DNSSEC is signed on the fly. Denial of existence uses NSEC black lies; NSEC3 is not supported. ECDSA is preferred because its signatures are smaller. The plugin can be used once per server block; with several in one zone, the last wins.

```
dnssec [ZONES...] {
    key file|aws_secretsmanager KEY...
    cache_capacity CAPACITY
}
```

- `key file` reads key files. Generate with `dnssec-keygen -a ECDSAP256SHA256 <zonename>`; a key for zone A may be used for zone B. Name the base `Kexample.org+013+45330` or the .key or .private file.
- `key aws_secretsmanager` reads secrets (names or ARNs) from AWS Secrets Manager, authenticated by the AWS SDK for Go V2; the credentials need `secretsmanager:GetSecretValue`.
- Mode: if there is at least one key with the SEP bit set and one without, signing splits ZSK/KSK; DNSKEY is signed by SEP keys, other records by non-SEP keys. Otherwise each key is a CSK.
- RRSIGs always use a TTL of 3600s because the original TTL is unknown.
- `cache_capacity` for stored RRSIGs defaults to 10000.

Example: `dnssec { key file Kexample.org+013+45330 }` in an `example.org` block with whoami.

## Checked

2026-11-03. Page read: https://coredns.io/plugins/dnssec/ (the CoreDNS plugin page).

Confirmed: the syntax, options, defaults, limits, metric names and examples stated in this skill.

Removed or corrected: nothing.

Method: documentation only; no commands were run.
