---
id: computing-software.cloud-infrastructure-engineering.google-cloud.private-google-access-for-on-premises-hosts
name: private-google-access-for-on-premises-hosts
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, private-google-access, private-google-access-on-premises, private-googleapis, cloud-router-advertisement, hybrid-dns]
level: practitioner
status: docs-checked
description: "Let on-prem hosts reach Google APIs privately over VPN or Interconnect: advertise private/restricted VIP ranges via Cloud Router, on-prem DNS for googleapis.com, and testing."
sources: ["https://docs.cloud.google.com/vpc/docs/configure-private-google-access-hybrid", "https://docs.cloud.google.com/vpc/docs/configure-private-google-access"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Private Google Access for on-premises hosts

## 1. Pick the VIP
| Domain | VIP range | Use |
|---|---|---|
| `private.googleapis.com` | `199.36.153.8/30` | most Google APIs |
| `restricted.googleapis.com` | `199.36.153.4/30` | only VPC-SC-supported APIs, for perimeters |

## 2. Advertise the range to on-prem
```bash
gcloud compute routers update cr-ew2 --region=europe-west2 \
  --advertisement-mode=CUSTOM --set-advertisement-groups=ALL_SUBNETS \
  --set-advertisement-ranges=199.36.153.8/30
```
(Or advertise per BGP session instead of per router.) The VPC network also needs a route for the VIP range with next hop
default internet gateway. A default route (`0.0.0.0/0`) with that next hop satisfies this; Google does not publish these
ranges on the internet, so the packets stay inside Google's network.

## 3. DNS on-prem
Make `*.googleapis.com` resolve to the VIP for on-prem clients by creating a `googleapis.com`
zone on the on-prem DNS servers:
```
private.googleapis.com.  A 199.36.153.8 199.36.153.9 199.36.153.10 199.36.153.11
*.googleapis.com.        CNAME private.googleapis.com.
```
Other domains (`*.gcr.io`, `*.gstatic.com`, `*.pkg.dev`, `pki.goog`, `*.run.app`, `*.gke.goog`) need their own zone with an A
record to the same VIPs plus a `*.DOMAIN` CNAME to `DOMAIN`, if the domain is reachable through that VIP (see the domain
options table). Alternatively, forward these zones from on-prem DNS to a Cloud DNS inbound server policy where the private zones live.

## 4. On-prem routing
On-prem needs routes for the VIP range pointing at the Cloud VPN tunnel or VLAN attachment.

## Test
```bash
dig +short storage.googleapis.com           # 199.36.153.x
```

## Gotchas
- Without the custom advertisement, on-prem has no route to the VIP range even though DNS points to it.
- `restricted.googleapis.com` denies Google APIs not supported by VPC Service Controls, so some tools break.
- Private Service Connect endpoints for Google APIs are the alternative with your own IP.

## Verify
- [ ] On-prem host lists a bucket with traffic over the tunnel (VPN metrics increase), no internet egress.

## Checked
2026-10-28. Confirmed against "Configure Private Google Access for on-premises hosts": VIP ranges and A records, `*.googleapis.com` CNAME,
extra domains list, default-internet-gateway next hop, Cloud Router custom advertisements, restricted VIP and VPC Service Controls.
Commands verified against the gcloud reference. Removed: firewall/proxy 443 advice, traceroute and curl tests, `--advertised-route-priority`.
Method: documentation only; no commands were run.
