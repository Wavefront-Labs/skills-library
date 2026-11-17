---
id: computing-software.cloud-infrastructure-engineering.google-cloud.private-google-access-dns-and-vips
name: private-google-access-dns-and-vips
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, private-google-access, private-googleapis-vip, restricted-vip, private-google-access-dns, vpc-service-controls]
level: advanced
status: docs-checked
description: "Reach Google APIs privately from VPCs and on-prem: private vs restricted googleapis.com VIPs, Cloud DNS private zones, routes, and advertising VIP ranges over hybrid links."
sources: ["https://docs.cloud.google.com/vpc/docs/configure-private-google-access", "https://docs.cloud.google.com/vpc/docs/configure-private-google-access-hybrid"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Private Google Access DNS and VIPs

## 1. Pick the VIP
| Domain | IPv4 range | Use |
|---|---|---|
| `private.googleapis.com` | 199.36.153.8/30 | most Google APIs, not limited to VPC-SC-supported ones |
| `restricted.googleapis.com` | 199.36.153.4/30 | only VPC-SC-supported APIs; use with service perimeters to block exfiltration to non-perimeter APIs |
IPv6: `2600:2d00:0002:2000::/56` (private) and `2600:2d00:0002:1000::/56` (restricted); add AAAA records pointing to
`2600:2d00:0002:2000::` or `2600:2d00:0002:1000::` to use them.

## 2. DNS
```bash
gcloud dns managed-zones create googleapis --dns-name=googleapis.com. --visibility=private \
  --networks=<VPC> --description="PGA restricted VIP"
gcloud dns record-sets create restricted.googleapis.com. --zone=googleapis --type=A --ttl=300 \
  --rrdatas=199.36.153.4,199.36.153.5,199.36.153.6,199.36.153.7
gcloud dns record-sets create '*.googleapis.com.' --zone=googleapis --type=CNAME --ttl=300 \
  --rrdatas=restricted.googleapis.com.
```
Add similar zones (A record to the VIP, `*.DOMAIN` CNAME to `DOMAIN`) for other domains your workloads use, such as
`gcr.io`, `pkg.dev`, `run.app`; check the "domain options" table to see which VIP serves each.

## 3. Routing
- Subnets: `gcloud compute networks subnets update <S> --region=<R> --enable-private-ip-google-access`.
- Routes whose next hop is the default internet gateway must exist; a default route (0.0.0.0/0) with that next hop covers it.
  Traffic stays inside Google's network. If you replaced the default route, add routes for the VIP range.

## 4. On-prem
Advertise the VIP range from Cloud Router (custom advertisement `199.36.153.4/30`), and make on-prem
DNS forward `googleapis.com` to a Cloud DNS inbound forwarder (inbound server policy) or host the same records on-prem.

## Gotchas
- A VM with an external IP does not need Private Google Access to reach Google APIs.
- `*.googleapis.com` CNAME to restricted denies APIs not supported by VPC Service Controls: use the private VIP for those.
- PSC endpoints for Google APIs are the alternative when you need your own internal IP.

## Verify
- [ ] From a VM: `dig storage.googleapis.com` returns 199.36.153.4 to .7 and API calls succeed without an external IP.

## Checked
2026-10-28. Confirmed against "Configure Private Google Access" and its on-premises page: both VIP ranges, IPv6 /56 ranges and AAAA targets,
CNAME pattern, default internet gateway next hop, external-IP VMs, restricted VIP and VPC Service Controls. gcloud commands verified
against the reference. Removed: egress firewall advice (not stated), IPv6 /64 sizes (docs say /56).
Method: documentation only; no commands were run.
