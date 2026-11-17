---
id: computing-software.cloud-infrastructure-engineering.external-dns.ingress-source-names-and-targets
name: ingress-source-names-and-targets
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, ingress-source, ingress-class, ignore-ingress-rules-spec, ignore-ingress-tls-spec]
level: practitioner
status: docs-checked
description: "How the ExternalDNS ingress source picks hostnames from rules, TLS hosts, annotations and templates, how targets come from status or annotation, and the ingress-class filter."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/sources/ingress.md
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/annotations/annotations.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ingress source

Creates DNS entries from `Ingress.networking.k8s.io`.

**Filtering:** `--ingress-class` (repeatable for several classes) and `--label-filter`.

**Hostnames, in order**
1. Each non-empty `host` in `spec.rules`. Suppressed by `--ignore-ingress-rules-spec` or by `ingress-hostname-source: annotation-only`.
2. Each entry in `spec.tls[].hosts`. Suppressed by `--ignore-ingress-tls-spec` or `annotation-only`.
3. The `external-dns.kubernetes.io/hostname` annotation. Suppressed by `--ignore-hostname-annotation` or `ingress-hostname-source: defined-hosts-only`.
4. `--fqdn-template` names, if steps 1 to 3 produced nothing or `--combine-fqdn-annotation` is set.

**Targets**
1. The `external-dns.kubernetes.io/target` annotation, if present.
2. Otherwise each non-empty `ip` and `hostname` in `status.loadBalancer.ingress`.

For the `target` annotation, IPv4 values become A records, IPv6 values AAAA records, and anything else CNAME records.

**Gotchas**
- TLS hosts create records even if no rule uses them, unless suppressed.
- Setting `--ignore-hostname-annotation` stops the hostname annotation being read.

## Checked

2026-11-04. Confirmed against the ExternalDNS Ingress source page (filtering, hostname order, targets) and the annotations page (target annotation record types). Removed an unsourced gotcha, a verification line, and an unsupported claim about status-derived record types.
Method: documentation only; no commands were run.
