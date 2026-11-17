---
id: computing-software.cloud-infrastructure-engineering.external-dns.multi-cluster-shared-record-patterns
name: multi-cluster-shared-record-patterns
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, multi-cluster, shared-hostname, dnsendpoint-aggregate, weighted-routing, coredns-strictly-owned]
level: sme
status: docs-checked
description: "Publish one hostname from several clusters with ExternalDNS: four supported patterns (aggregate, single owner, Route53 set identifiers, CoreDNS) and the unsupported target merge."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/advanced/multi-cluster-shared-records.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-cluster shared records

Every pattern needs a distinct `--txt-owner-id` per cluster.

- **A, aggregate (any provider):** each cluster publishes `app.eu.example.com` and `app.us.example.com`; one designated cluster holds a `DNSEndpoint` for `app.example.com` of type A with all LB addresses. It must be A, not a multi-target CNAME (a CNAME must be the only record for its name, RFC 1034 section 3.6.2). Edit it when addresses change.
- **B, single owner (any provider):** only one cluster manages the name; exclude it elsewhere with `--domain-filter`, `--annotation-filter` or `--label-filter`, or just do not annotate it. Add `--policy=upsert-only` on non-owners for defence in depth.
- **C, Route 53 only:** same hostname, distinct `set-identifier` and a routing policy per cluster:
  ```yaml
  external-dns.kubernetes.io/hostname: app.example.com
  external-dns.kubernetes.io/set-identifier: cluster-a
  external-dns.kubernetes.io/aws-weight: "50"
  ```
  Never set all weights to 0 (Route 53 then serves them). `aws-multi-value-answer` works only for non-alias records, for example with `--aws-prefer-cname` or plain IP targets. OCI warns and ignores `set-identifier`.
- **D, CoreDNS only:** `--coredns-strictly-owned` stamps an owner on every etcd entry so each instance sees only its own.

**Not supported:** two instances contributing targets to one record set under the TXT registry. The ownership TXT is per name with one owner; elsewhere, the first cluster owns the record and the second skips it forever.

**Why a second instance seems idle:** with `--log-level=debug` look for `Skipping endpoint ... because owner id does not match`. Creating under an owned name increments `external_dns_registry_skipped_records_owner_mismatch_per_sync`.

## Checked

2026-11-04. Confirmed against the ExternalDNS Multi-Cluster Shared DNS Records page: the four patterns, the RFC 1034 CNAME point, Route53 set-identifier and weight rules, multi-value alias limits, CoreDNS ownership and the unsupported merge. Nothing removed.
Method: documentation only; no commands were run.
