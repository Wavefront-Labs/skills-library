---
id: computing-software.cloud-infrastructure-engineering.external-dns.rfc2136-axfr-and-sync-policy
name: rfc2136-axfr-and-sync-policy
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, rfc2136-axfr, rfc2136-axfr-insecure, create-only-fallback, split-server-axfr]
level: advanced
status: docs-checked
description: "Why RFC2136 needs --rfc2136-axfr for sync, the silent create-only fallback, and --rfc2136-axfr-insecure for unsigned zone transfers with signed updates."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/tutorials/rfc2136.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AXFR and the sync policy (RFC2136)

ExternalDNS lists existing records over zone transfer. With `--policy=sync` you must set `--rfc2136-axfr`, otherwise it cannot list records and **acts as if the policy were `create-only`**. The docs also say deletions need it, and reading TLSA (or any other) records needs it.

**Unsigned AXFR with signed UPDATE.** When TSIG is configured, the key is used for both UPDATE and AXFR. In split-role setups (for example a hidden primary accepting signed updates while secondaries serve unsigned transfers) AXFR has no TSIG. Use:

```bash
--rfc2136-tsig-keyname=externaldns-key \
--rfc2136-tsig-secret=<secret> \
--rfc2136-tsig-secret-alg=hmac-sha256 \
--rfc2136-axfr \
--rfc2136-axfr-insecure
```

| `--rfc2136-insecure` | `--rfc2136-gss-tsig` | `--rfc2136-axfr-insecure` | UPDATE | AXFR |
|---|---|---|---|---|
| no | no | no | HMAC TSIG | HMAC TSIG |
| no | no | yes | HMAC TSIG | none |
| yes | no | any | none | none |
| no | yes | any | GSS-TSIG | none |

- Zone transfer responses are then unauthenticated: use a trusted network path or combine with `--rfc2136-use-tls`.
- It is a no-op under `--rfc2136-insecure` or `--rfc2136-gss-tsig`.
- It requires `--rfc2136-axfr`; without it startup is rejected. The deprecated `--rfc2136-tsig-axfr` also satisfies this.

**Symptom check:** if records are never deleted under `sync`, confirm `--rfc2136-axfr` and that the key may transfer the zone.

## Checked

2026-11-04. Read the RFC2136 tutorial (AXFR and the sync policy, Unsigned zone transfers, TLSA caveats, insecure and GSS-TSIG examples). Confirmed the create-only fallback without --rfc2136-axfr, the axfr-insecure behaviour, the auth table, the no-op cases, the startup rejection and the deprecated --rfc2136-tsig-axfr note. Removed nothing.

Method: documentation only; no commands were run.
