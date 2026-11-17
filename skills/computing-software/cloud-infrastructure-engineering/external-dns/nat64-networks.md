---
id: computing-software.cloud-infrastructure-engineering.external-dns.nat64-networks
name: nat64-networks
category: computing-software
field: cloud-infrastructure-engineering
product: external-dns
tags: [external-dns, nat64-networks, siit, ipv6-only-nodes, a-record-synthesis]
level: advanced
status: docs-checked
description: "Create extra A records for IPv6-only nodes behind NAT64/SIIT with --nat64-networks, which must be /96 prefixes."
sources:
  - https://raw.githubusercontent.com/kubernetes-sigs/external-dns/master/docs/advanced/nat64.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NAT64 networks

When NAT64 is handled outside the cluster, Kubernetes knows nothing of the associated IPv4 addresses. `--nat64-networks` lets ExternalDNS create an A record with the NAT64-translated IPv4 address for each AAAA record whose IPv6 target falls in the given network.

```sh
--nat64-networks="2001:db8:96::/96"
```

- Each network **must** be a /96.
- Pass several by comma-separating them.

**Docs setup:** nodes have only IPv6 addresses but reach, and are reached from, IPv4 through an external NAT64 resolver using SIIT (Stateless IP/ICMP Translation). Outgoing traffic is classic NAT64 into a small IPv4 pool. Incoming traffic maps a different IPv4 pool, such as `198.51.100.0/24`, one-to-one to IPv6. Dedicate a /96 (for example `2001:db8:96::/96`), so `198.51.100.0/24` translates to `2001:db8:96::c633:6400/120` (a /120 has as many addresses as a /24).

Then `2001:db8:96::c633:640a` (also written `2001:0DB8:96::198.51.100.10`) translates to `198.51.100.10`.

Any source can point a record at an IPv6 address inside the network. The result is the default AAAA record plus, because `nat64-networks` is set, an A record with `198.51.100.10`.

## Checked

2026-11-04. Confirmed against the ExternalDNS Configure NAT64 DNS Records page: /96 requirement, comma-separated networks, setup example and address translation. Removed an unsourced dig verification line.
Method: documentation only; no commands were run.
