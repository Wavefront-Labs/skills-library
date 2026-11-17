---
id: computing-software.cloud-infrastructure-engineering.aws.cloud-wan-and-network-manager
name: cloud-wan-and-network-manager
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, cloud-wan, network-manager, core-network, global-network, segments, transit-gateway, multi-region]
level: practitioner
status: draft
description: "Run a multi-region WAN with AWS Cloud WAN: global network, core network policy (segments, edge locations, attachment policies), TGW integration, and Network Manager monitoring."
sources: ["https://docs.aws.amazon.com/network-manager/latest/cloudwan/what-is-cloudwan.html", "https://docs.aws.amazon.com/network-manager/latest/cloudwan/cloudwan-policy-change-sets.html", "https://docs.aws.amazon.com/network-manager/latest/tgwnm/what-are-global-networks.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cloud WAN and Network Manager

**When:** several regions, many VPCs and sites, and you are tired of hand-maintaining TGW
peering meshes and static routes. Cloud WAN gives one policy document for global routing.

## 1. Concepts
- **Global network**: container (also used by TGW Network Manager for monitoring existing TGWs).
- **Core network**: the AWS-managed WAN; **core network edges** in chosen regions.
- **Segments**: isolated routing domains (like VRFs): `prod`, `dev`, `shared`.
- **Attachment policies**: rules mapping attachments (by tag, account, region) to segments.

## 2. Core network policy (excerpt)
```json
{
  "version": "2021.12",
  "core-network-configuration": {"asn-ranges": ["64512-64555"],
    "edge-locations": [{"location": "us-east-1"}, {"location": "eu-west-1"}]},
  "segments": [
    {"name": "prod", "require-attachment-acceptance": true},
    {"name": "dev", "require-attachment-acceptance": false},
    {"name": "shared"}],
  "segment-actions": [
    {"action": "share", "mode": "attachment-route", "segment": "shared", "share-with": ["prod", "dev"]}],
  "attachment-policies": [
    {"rule-number": 100, "conditions": [{"type": "tag-value", "key": "segment", "operator": "equals", "value": "prod"}],
     "action": {"association-method": "constant", "segment": "prod"}},
    {"rule-number": 200, "conditions": [{"type": "tag-exists", "key": "segment"}],
     "action": {"association-method": "tag", "tag-value-of-key": "segment"}}]
}
```
```bash
aws networkmanager put-core-network-policy --core-network-id core-network-0abc --policy-document file://policy.json
aws networkmanager get-core-network-change-set --core-network-id core-network-0abc --policy-version-id 3
aws networkmanager execute-core-network-change-set --core-network-id core-network-0abc --policy-version-id 3
```
Review the change set like a Terraform plan before executing.

## 3. Attaching
VPC attachments (`create-vpc-attachment` with the segment tag), site-to-site VPN, Connect
(SD-WAN GRE/tunnel-less), and **TGW route table attachments** via TGW peering to migrate
existing TGW estates gradually.

## 4. Network Manager for existing TGWs
Register TGWs in a global network to get a topology map, **Route Analyzer**, events and
CloudWatch metrics across regions — useful even without Cloud WAN.

## Gotchas
- Segments isolate by default; sharing is explicit (`segment-actions`).
- Policy changes are global; a bad attachment policy can move attachments between segments —
  `require-attachment-acceptance` on prod.
- Pricing: per core network edge hour, per attachment hour and per GB — compare with TGW.

## Verify
- [ ] `get-core-network` shows edges in every intended region and state `AVAILABLE`.
- [ ] A prod-tagged VPC lands in segment `prod`; route from prod to dev absent; prod to shared present.
- [ ] Route Analyzer path between two regions' VPCs is `Connected` via the core network.
