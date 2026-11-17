---
id: computing-software.cloud-infrastructure-engineering.metallb.pool-auto-assign-and-buggy-ips
name: pool-auto-assign-and-buggy-ips
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, autoassign, avoidbuggyips, ipaddresspool, smurf-protection, expensive-ips]
level: practitioner
status: docs-checked
description: "Reserve scarce MetalLB pools with autoAssign false so only explicit requests use them, and skip .0 and .255 addresses with avoidBuggyIPs for old consumer networks."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/configuration/_advanced_ipaddresspool_configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# autoAssign and avoidBuggyIPs

## autoAssign
By default MetalLB allocates from any pool with free addresses, which may burn "expensive" public IPs on services that do not need them. Set `autoAssign: false` on the scarce pool:
```yaml
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: expensive
  namespace: metallb-system
spec:
  addresses:
  - 42.176.25.64/30
  autoAssign: false
```
Addresses can still be requested explicitly (IP or pool) as in `computing-software.cloud-infrastructure-engineering.metallb.request-specific-ip-or-pool`. Single IP in a pool: `/32`.

## avoidBuggyIPs
Some old consumer network gear blocks addresses ending in `.0` and `.255` (misguided smurf protection). Set `avoidBuggyIPs: true` on the `IPAddressPool` and those two are skipped.

Note: a Service that requests a pool or IP via `metallb.io/address-pool`, `spec.loadBalancerIP` or `metallb.io/loadBalancerIPs` that does not match stays pending.

## Checked

2026-11-04. Confirmed against the MetalLB "Advanced AddressPool configuration" page (autoAssign example with 42.176.25.64/30, /32 for one IP, .0 and .255 buggy-network wording, pending note). The page names the flag `AvoidBuggyIPs` in prose and `avoidBuggyIPs: true` in its YAML example. Removed the unsupported Check line.

Method: documentation only; no commands were run.
