---
id: computing-software.systems-network-administration.netbird.extra-dns-labels
name: extra-dns-labels
category: computing-software
field: systems-network-administration
product: netbird
tags: [netbird, extra-dns-labels, wildcard-labels, round-robin-dns, nb-extra-dns-labels]
level: practitioner
status: docs-checked
description: "Add extra DNS names to a NetBird peer with --extra-dns-labels: setup key prerequisite, label rules, wildcards, round-robin sharing and clearing labels."
sources:
  - https://raw.githubusercontent.com/netbirdio/docs/main/src/pages/manage/dns/extra-dns-labels.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Extra labels give a peer additional DNS names beyond its hostname.

Prerequisite: a setup key with "Allow Extra DNS Labels" enabled, or the management server rejects labels at registration.

Assign:
```
netbird up --setup-key <KEY> --extra-dns-labels vpc1,api
```
Containers: set `NB_EXTRA_DNS_LABELS`. Each label creates a record under the peer DNS domain (e.g. `vpc1.netbird.cloud`) pointing to the peer's NetBird IP. Clear with `netbird up --extra-dns-labels ""`.

Rules: ASCII letters, digits, hyphens, underscores; Unicode is not converted to punycode; up to 32 labels per peer.

Wildcards: `"*.myserver"` matches one subdomain level (`app1.myserver.netbird.cloud`) but not multi-level names (RFC 4592). Handy for a reverse proxy serving several apps.

Round robin: peers sharing a label rotate through their IPs. DNS-level only, with no health checks, so an offline peer's IP may still be returned until it is removed.

## Checked

2026-11-04: read the Extra DNS Labels page in full. Confirmed the setup key prerequisite, flag and NB_EXTRA_DNS_LABELS usage, clearing with an empty string, label rules and the 32-label limit, wildcard single-level matching (RFC 4592) and the round-robin caveat. Nothing removed.

Method: documentation only; no commands were run.
