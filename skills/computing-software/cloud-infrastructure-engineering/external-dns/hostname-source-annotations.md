---
id: computing-software.cloud-infrastructure-engineering.external-dns.hostname-source-annotations
name: hostname-source-annotations
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, ingress-hostname-source, gateway-hostname-source, defined-hosts-only, annotation-only]
level: practitioner
status: docs-checked
description: "Control where ExternalDNS takes hostnames from with ingress-hostname-source and gateway-hostname-source: defined-hosts-only, annotation-only, or both."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/annotations/annotations.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hostname source annotations

Two annotations restrict where hostnames come from.

**`external-dns.kubernetes.io/ingress-hostname-source`** (on an `Ingress`):
- `defined-hosts-only`: use only domains from the Ingress spec.
- `annotation-only`: use only domains from the Ingress annotations (for example `hostname`).
- Absent: use both spec and annotations.

**`external-dns.kubernetes.io/gateway-hostname-source`** (on a Gateway API `Route`):
- `defined-hosts-only`: use only domains from the Route spec.
- `annotation-only`: use only domains from the Route annotations.
- Absent: use both.

Put the gateway annotation on the actual Route resource, not on the Gateway.

Example, to keep annotation-listed names only:

```yaml
metadata:
  annotations:
    external-dns.kubernetes.io/ingress-hostname-source: annotation-only
    external-dns.kubernetes.io/hostname: www.example.com
```

**Gotchas**
- Names still must match `--domain-filter`.
- With `annotation-only`, hosts in `spec.rules[].host` are ignored, so a rule without the annotation produces no record.
- Setting `--ignore-hostname-annotation` stops the `hostname` annotation being read at all.

## Checked

2026-11-04. Confirmed against the ExternalDNS annotations page (ingress-hostname-source, gateway-hostname-source and hostname sections, support-table footnote). Removed an unsourced log-verification line.
Method: documentation only; no commands were run.
