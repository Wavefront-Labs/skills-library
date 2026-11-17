---
id: computing-software.cloud-infrastructure-engineering.google-cloud.subnets-expansion-ipv6-internal-ranges-and-flow-logs
name: subnets-expansion-ipv6-internal-ranges-and-flow-logs
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, vpc, subnet-creation, expand-subnet, ipv6-subnets, dual-stack, internal-ranges, ip-address-management, flow-logs-enable, flow-logs-sampling]
level: practitioner
status: docs-checked
description: "Create and expand VPC subnets, add IPv6 dual-stack, reserve and allocate address space with internal ranges, and enable VPC Flow Logs with sensible sampling."
sources: ["https://docs.cloud.google.com/vpc/docs/create-modify-vpc-networks", "https://docs.cloud.google.com/vpc/docs/subnets/ipv6-ranges", "https://docs.cloud.google.com/vpc/docs/internal-ranges", "https://docs.cloud.google.com/vpc/docs/using-flow-logs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Subnets, expansion, IPv6, internal ranges and flow logs

## 1. Create
```bash
gcloud compute networks create prod --subnet-mode=custom --bgp-routing-mode=global --enable-ula-internal-ipv6
gcloud compute networks subnets create app-euw2 --network=prod --region=europe-west2 --range=10.10.0.0/22 \
  --secondary-range=pods=10.64.0.0/16,services=10.72.0.0/20 \
  --enable-private-ip-google-access \
  --stack-type=IPV4_IPV6 --ipv6-access-type=INTERNAL \
  --enable-flow-logs --logging-aggregation-interval=interval-5-sec --logging-flow-sampling=0.5 --logging-metadata=include-all
```

## 2. Expand (never shrink)
```bash
gcloud compute networks subnets expand-ip-range app-euw2 --region=europe-west2 --prefix-length=21
```
Expanding a primary IPv4 range cannot be undone and the range cannot be shrunk. Check the address space of every network
the VPC connects to before expanding, and leave adjacent space free in your IP plan.

## 3. IPv6
- `INTERNAL` IPv6 uses a /48 ULA from `fd20::/20` assigned to the VPC network (`--enable-ula-internal-ipv6`, optionally
  `--internal-ipv6-range`); each internal subnet gets an unused /64 from it.
- `EXTERNAL` IPv6 subnets get a /64 GUA range by default; a VM network interface is assigned a /96 range from its subnet.
- VMs: `--stack-type=IPV4_IPV6`.

## 4. Internal ranges (IPAM)
```bash
# reserve a block nobody may use for subnets (e.g. on-prem or future)
gcloud network-connectivity internal-ranges create reserved-onprem --network=prod \
  --ip-cidr-range=10.200.0.0/16 --usage=EXTERNAL_TO_VPC --peering=FOR_SELF
# let Google pick a free /22 for a new subnet
gcloud network-connectivity internal-ranges create app-next --network=prod --prefix-length=22 \
  --usage=FOR_VPC --peering=FOR_SELF --target-cidr-range=10.10.0.0/16
gcloud network-connectivity internal-ranges list
```
`FOR_VPC` (the default) means the range can be associated with other Google Cloud resources in its VPC network;
`EXTERNAL_TO_VPC` ranges cannot. `FOR_SELF` limits the block to the VPC where it was created.

## 5. Flow log sampling
Defaults: aggregation interval `interval-5-sec` (others: 30-sec, 1-min, 5-min, 10-min, 15-min), sampling 0.5
(range 0.0 to 1.0), metadata `include-all`. For large subnets raise the interval, lower the sampling rate, or add
`--logging-filter-expr` to reduce log volume.

## Gotchas
- Expansion is one-way; check IPAM first.
- Higher sampling and shorter intervals generate more log volume (see the vendor's pricing page for cost).

## Verify
- [ ] `gcloud compute networks subnets describe app-euw2 --region=<R> --format='yaml(ipCidrRange,stackType,logConfig)'`.
- [ ] Internal ranges list shows the reserved blocks.

## Checked
2026-10-28. Confirmed against the VPC pages on subnet IPv6 ranges, creating/expanding subnets, internal ranges and using flow logs:
fd20::/20 and /48 ULA, /64 subnet and /96 NIC ranges, no shrinking, flow-log intervals/sampling/metadata defaults, FOR_VPC default,
EXTERNAL_TO_VPC, FOR_SELF. Commands verified against the gcloud reference. Removed: pricing-style cost claims, secondary-range expansion,
/16 advice, `vpc_flows` log name, overlap-failure claim, firewall `::/0` claim.
Method: documentation only; no commands were run.
