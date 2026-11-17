---
id: computing-software.cloud-infrastructure-engineering.external-dns.coredns-strictly-owned-and-groups
name: coredns-strictly-owned-and-groups
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, coredns-provider, coredns-strictly-owned, etcd-owner-field, coredns-groups]
level: advanced
status: docs-checked
description: "CoreDNS provider on shared etcd: --coredns-strictly-owned with txt-owner-id for multi-cluster isolation, ownerless entry trap, migration options and service groups."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/tutorials/coredns.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CoreDNS provider: ownership and groups

**Multi-cluster on one etcd.** Set `--coredns-strictly-owned` plus a distinct `--txt-owner-id` per cluster. The provider then refuses to update, create or delete records owned by someone else, and refuses to load them. CoreDNS needs no change; it ignores the `owner` field in the etcd record.

**Trap:** service entries in etcd with no `owner` field are filtered out under `strictly-owned`. Enabling it later hides those entries because their owner is empty.

**Migrating to a multi-cluster setup** (two ways):
1. Add the correct `owner` field to the JSON of every service entry in etcd.
2. Remove all service entries and let the provider recreate them after a restart (possible downtime).

**Groups.** A service annotation can put services into groups to limit recursion, so a lookup returns only a subset. Example from the docs: `domain.local` should return 127.0.0.1 and 127.0.0.2, while `subdom.domain.local` returns 127.0.0.3 and 127.0.0.4. The two sets must be in different groups; the group names do not matter, only that members of one answer set share a group different from the other. A service found without a group is always included.

## Checked

2026-11-04. Confirmed against the ExternalDNS CoreDNS tutorial (multi cluster support, other etcd entries, migration ways, groups). Removed an unsourced cross-reference sentence.
Method: documentation only; no commands were run.
