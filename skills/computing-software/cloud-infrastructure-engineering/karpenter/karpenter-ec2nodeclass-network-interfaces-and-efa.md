---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-ec2nodeclass-network-interfaces-and-efa
name: karpenter-ec2nodeclass-network-interfaces-and-efa
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [networkinterfaces, efa, efa-only, networkcardindex, deviceindex, associatepublicipaddress, ipprefixcount]
level: advanced
status: docs-checked
description: "networkInterfaces for EFA workloads (interface vs efa-only), associatePublicIPAddress override and its multi-EFA restriction, ipPrefixCount and detailedMonitoring."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/nodeclasses.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# EC2NodeClass network interfaces and EFA

Optional `spec.networkInterfaces` configures network interface attachments, including EFA for HPC and ML. Fields: `networkCardIndex`, `deviceIndex`, `interfaceType`. The page gives no ranges or defaults for the indexes.

```yaml
spec:
  networkInterfaces:
    - networkCardIndex: 0
      deviceIndex: 0
      interfaceType: "interface"
    - networkCardIndex: 0
      deviceIndex: 1
      interfaceType: "efa-only"
```

- `interface`: standard ENA interface with IP connectivity.
- `efa-only`: EFA device for RDMA without an IP address.

`spec.associatePublicIPAddress` (boolean): when set it overrides the subnet `MapPublicIpOnLaunch`; when unset the subnet setting applies. It can be set to `false` for private-only subnets. Warning: if a NodeClaim requests multiple EFA resources and this is `true`, the instance fails to launch because of an EC2 restriction. The page recommends a separate NodePool and EC2NodeClass for EFA workloads.

`spec.ipPrefixCount` (integer): how many IP prefixes are assigned to the NodeClaim, mapped to `ipv4PrefixCount` on IPv4 clusters and `ipv6PrefixCount` on IPv6 clusters. No default is given.

`spec.detailedMonitoring: true` makes the EC2 console show monitoring graphs with a 1-minute period for launched instances.

## Checked
Method: 2026-11-08 read the Karpenter v1.13 nodeclasses.md page; removed the claim that Karpenter previously set `false` automatically for private subnets and the "consuming no IP address" EC2 detail beyond the page's wording. Field behaviour otherwise unchanged.
