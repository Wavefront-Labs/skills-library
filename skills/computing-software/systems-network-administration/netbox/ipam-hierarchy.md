---
id: computing-software.systems-network-administration.netbox.ipam-hierarchy
name: ipam-hierarchy
category: computing-software
field: systems-network-administration
product: netbox
tags: [ipam, aggregate, prefix-hierarchy]
level: practitioner
status: docs-checked
description: "Use aggregates, prefixes, ranges and addresses and let NetBox build the tree."
sources: ["https://netboxlabs.com/docs/netbox/features/ipam/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# IPAM hierarchy

Goal: represent address space without manually linking parents.

NetBox supports full IPv4 and IPv6 parity. Four object types form the hierarchy:

- **Aggregate**: root of an addressing hierarchy, typically a large public or private allocation, assigned to an authoritative RIR.
- **Prefix**: a subnet within an aggregate. Prefixes nest inside one another and can carry a functional role.
- **IP range**: an arbitrary run of addresses within a prefix, all sharing one mask. Often used for DHCP scopes.
- **IP address**: an address with its mask, arranged beneath its parent prefix.

Parents are never assigned by hand. Hierarchies form automatically from the rules of IP addressing. Example from the docs:

```
100.64.0.0/10 (aggregate)
  100.64.16.0/20 (prefix)
    100.64.16.0/24 (prefix)
      100.64.16.1/24 (address)
      100.64.32.10-99/24 (range)
```

**Utilization.** It is calculated automatically by status. Container prefixes, which house child prefixes, are measured by how much of their space children consume. Aggregate utilization is the space consumed by child prefixes.

**AS numbers.** NetBox also tracks 16- and 32-bit ASNs, each assigned to an RIR and to sites.

**Checklist**

1. Create aggregates first for owned space.
2. Add prefixes and let nesting happen.
3. Use ranges for DHCP scopes.
4. Read utilization instead of computing it.

## Checked

2026-11-03: confirmed against the cited NetBox documentation: IPAM feature page: aggregate/prefix/range/IP address hierarchy, automatic parenting, utilization, 16- and 32-bit ASNs. Removed: Nothing.

Method: documentation only; no commands were run.
