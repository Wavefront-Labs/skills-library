---
id: computing-software.cloud-infrastructure-engineering.external-dns.annotation-prefix-and-legacy-migration
name: annotation-prefix-and-legacy-migration
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, annotation-prefix, enable-legacy-annotation-prefix, alpha-annotation, annotation-filter]
level: practitioner
status: docs-checked
description: "ExternalDNS annotation prefix: default external-dns.kubernetes.io/, the pre-v0.22.0 alpha prefix, and the --enable-legacy-annotation-prefix migration aid."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/annotations/annotations.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Annotation prefix and legacy migration

All annotations use the prefix from `--annotation-prefix`, default `external-dns.kubernetes.io/`. Releases before v0.22.0 used `external-dns.alpha.kubernetes.io/`.

**Gradual migration:** `--enable-legacy-annotation-prefix` adds the configured-prefix equivalent of every legacy-prefixed annotation before any filter, indexer or source reads the resource.

- The legacy key is kept, so an `--annotation-filter` or template written against either prefix keeps matching.
- On conflict the configured prefix wins, and the ignored value is logged with the resource.
- Nothing is written back to the cluster, so manifests are not changed.
- It is a migration aid that will be removed in a future release. Drop the flag once no resource uses the legacy prefix.

**Steps**
1. Start ExternalDNS with `--enable-legacy-annotation-prefix`.
2. Rewrite manifests from `external-dns.alpha.kubernetes.io/hostname` to `external-dns.kubernetes.io/hostname`.
3. Read the logs for ignored-value messages, which show a conflict between old and new values.
4. Remove the flag when nothing uses the legacy prefix.

**Gotcha:** the docs describe the `hostname` annotation as alpha and subject to change. Provider annotations use their own sub-prefixes such as `external-dns.kubernetes.io/aws-`, `azure-`, `cloudflare-` and `scw-`.

## Checked

2026-11-04. Confirmed against the ExternalDNS annotations page (Annotation prefix section and provider prefix table): default prefix, pre-v0.22.0 alpha prefix, the legacy-prefix flag behaviour, and the sub-prefixes.
Method: documentation only; no commands were run.
