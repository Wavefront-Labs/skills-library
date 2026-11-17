---
id: computing-software.cloud-infrastructure-engineering.external-dns.split-horizon-annotation-prefix
name: split-horizon-annotation-prefix
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, split-horizon, annotation-prefix-flag, internal-external-dns, multiple-instances]
level: advanced
status: docs-checked
description: "Run several ExternalDNS instances with different --annotation-prefix values for split-horizon DNS, with per-instance owners, helm values and the trailing-slash rule."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/advanced/split-horizon.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Split horizon with annotation prefixes

Serve private IPs to internal clients and public IPs to external ones by running one ExternalDNS per audience, each with its own `--annotation-prefix`.

```bash
# internal
external-dns --annotation-prefix=internal.company.io/ --source=service --source=ingress \
  --provider=aws --aws-zone-type=private --domain-filter=internal.company.com --txt-owner-id=internal-dns
# external (default prefix)
external-dns --source=service --source=ingress \
  --provider=aws --aws-zone-type=public --domain-filter=company.com --txt-owner-id=external-dns
```

One Service carries both sets:
```yaml
annotations:
  internal.company.io/hostname: myapp.internal.company.com
  internal.company.io/target: 10.0.1.50
  external-dns.kubernetes.io/hostname: myapp.company.com
```
With no `target` the external instance uses the LoadBalancer IP.

**Rules**
- The prefix must end with `/`; otherwise validation fails (`annotation-prefix must end with '/'`).
- Once set, all annotations for that instance use the prefix, including `ttl`, `target` and provider ones such as `custom.io/cloudflare-proxied`.
- Give every instance a unique `--txt-owner-id`.
- Helm: set `annotationPrefix`, `txtOwnerId`, `domainFilters` and provider values per release; the docs install each release into its own namespace.

The pattern extends to three-way (internal, DMZ, external) and to different providers per instance. If both instances act on one resource, check the resource uses distinct prefixes and that duplicate keys did not overwrite each other.

## Checked

2026-11-04. Confirmed against the ExternalDNS Split Horizon DNS page: overview, internal and external commands, the two-prefix Service, Helm values, important notes and troubleshooting. Nothing removed.
Method: documentation only; no commands were run.
