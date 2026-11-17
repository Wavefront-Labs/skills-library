---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-ec2nodeclass-imds-and-connection-tracking
name: karpenter-ec2nodeclass-imds-and-connection-tracking
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [metadataoptions, imds, httptokens, hop-limit, connectiontracking, nitro, tcpestablishedtimeout, udptimeout]
level: advanced
status: docs-checked
description: "metadataOptions IMDS defaults (hop limit 1, tokens required) and connectionTracking timeouts with valid ranges and defaults, Nitro-only effect and ENI scope."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/nodeclasses.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# EC2NodeClass metadataOptions and connectionTracking

`spec.metadataOptions` (optional) controls IMDS on launched instances via the generated launch template. Defaults if omitted:

```yaml
metadataOptions:
  httpEndpoint: enabled
  httpProtocolIPv6: disabled
  httpPutResponseHopLimit: 1   # disables IMDS access from containers not on the host network
  httpTokens: required
```

The page links to security best practices for limiting exposure of instance metadata and user data to pods. It does not give the valid range for `httpPutResponseHopLimit`.

`spec.connectionTracking` (optional) sets security group connection tracking timeouts, integer seconds, on Karpenter-provisioned ENIs: the primary ENI, EFA ENIs and `interface`-type network interfaces. `efa-only` interfaces are not covered. ENIs created later by your CNI (the page names VPC CNI and Cilium in ENI IPAM mode) are out of scope and must be configured through the CNI. Setting it makes Karpenter exclude non-Nitro instance types. Unset fields use EC2 defaults.

| Field | Range | Default per page |
|---|---|---|
| `tcpEstablishedTimeout` | 60-432000 | 350 on Nitro v6 (excluding P6e-GB200), 432000 otherwise (the page's own example comment cites 432000 without that distinction) |
| `udpStreamTimeout` | 60-180 | 180 |
| `udpTimeout` | 30-60 | 30 |

```yaml
connectionTracking:
  tcpEstablishedTimeout: 300
  udpStreamTimeout: 120
  udpTimeout: 45
```

Purpose, from the page: idle connections left too long can exhaust the security group's connection tracking table and lead to dropped packets.

## Checked
Method: 2026-11-08 read the Karpenter v1.13 nodeclasses.md page; removed the advice to raise the hop limit only when pods need IMDS and the claim that lower timeouts cost long-lived idle flows (not stated); noted the page's inconsistent TCP default wording. Defaults and ranges unchanged.
