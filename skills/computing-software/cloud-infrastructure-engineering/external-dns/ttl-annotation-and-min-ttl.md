---
id: computing-software.cloud-infrastructure-engineering.external-dns.ttl-annotation-and-min-ttl
name: ttl-annotation-and-min-ttl
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, min-ttl, ttl-duration, ttl-provider-support, record-ttl]
level: practitioner
status: docs-checked
description: "Set record TTL in ExternalDNS with the ttl annotation or --min-ttl, in seconds or Go durations, plus which providers and sources honour it and their zero-TTL defaults."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/advanced/ttl.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TTL: annotation, --min-ttl and provider defaults

Set TTL per resource with the annotation, or a floor with `--min-ttl=<duration>`. The value is seconds or a Go duration (`1s`, `1m2s`, `1h2m11s`, parsed by `time.ParseDuration`). `"60"` and `"1m"` are equal. It must be positive.

```yaml
metadata:
  annotations:
    external-dns.kubernetes.io/hostname: nginx.external-dns-test.my-org.com.
    external-dns.kubernetes.io/ttl: "60"
```

**Behaviour**
- Annotation set: overrides the default TTL of 0 (meaning not configured).
- Annotation absent: default applies, unless `--min-ttl` is given.
- Annotation `0` with `--min-ttl=1s`: the `--min-ttl` value is used.
- The `hostname` annotation must also be set, and both source and provider must support TTL.

**Zero-TTL provider behaviour**
- AWS: overrides 0 to 300s (a constant). Google: also 300s. Neither can use 0.
- Azure: 1 to 2,147,483,647 seconds, default 300s.
- Cloudflare: 0 becomes "auto".
- DNSimple: default 3600s.

**Providers that do not support custom TTL:** Civo, CoreDNS, InMemory, NS1, OVH, PDNS. Sources that do not: connector, crd, empty, fake. The TTL page lists the pod source as supported, but the annotations page table shows no ttl for Pod, so test it before relying on it.

**Use cases:** low TTL (for example `30s`) for failover and blue/green; long TTL (`24h`) for static services; short TTL on autoscaling GCP node pools, where the default 300s can leave stale node records for minutes.

**Verify:** `dig <name>` and read the TTL column.

## Checked

2026-11-04. Read the TTL page (behaviour list, provider and source support tables, Notes on AWS, Azure, Cloudflare, DNSimple and Google, use cases). Confirmed the duration formats, positive-value rule, --min-ttl behaviour, the zero-TTL defaults per provider and the unsupported provider and source lists. Added a note that the annotations page disagrees on the Pod source.

Method: documentation only; no commands were run.
