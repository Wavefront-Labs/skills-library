---
id: computing-software.cloud-infrastructure-engineering.google-cloud.ordering-dedicated-interconnect-and-loa-cfa
name: ordering-dedicated-interconnect-and-loa-cfa
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, hybrid-connectivity, interconnect-ordering, loa-cfac, dedicated-interconnect, vlan-attachments]
level: advanced
status: docs-checked
description: "Order Dedicated Interconnect: pick colocation facilities for 99.99% topology, request links, use the LOA-CFA for cross-connects, test, then create VLAN attachments and BGP."
sources: ["https://cloud.google.com/network-connectivity/docs/interconnect/how-to/dedicated/ordering-dedicated-interconnect", "https://cloud.google.com/network-connectivity/docs/interconnect/how-to/dedicated/retrieving-loas", "https://cloud.google.com/network-connectivity/docs/interconnect/tutorials/dedicated-creating-9999-availability", "https://cloud.google.com/network-connectivity/docs/interconnect/how-to/dedicated/provisioning-overview", "https://cloud.google.com/network-connectivity/docs/interconnect/concepts/dedicated-overview", "https://cloud.google.com/sdk/gcloud/reference/compute/interconnects/attachments/dedicated/create"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ordering Dedicated Interconnect and the LOA-CFA

## 1. Plan topology
- 99.99% (multi-region): at least four connections in two metros, using both edge availability domains (zone 1 and zone 2) of each metro. A single-region 99.99% configuration also exists; see the 99.99% tutorial.
- 99.9%: two connections in one metro in different edge availability domains.
- Link capacity 10 Gbps, 100 Gbps or 400 Gbps per circuit; a connection bundles up to 8 circuits (8 x 10G, 8 x 100G or 8 x 400G).
- If you aren't in a supported colocation facility, use Partner Interconnect instead.

## 2. Order
```bash
gcloud compute interconnects locations list
gcloud compute interconnects create ic-ash-1 --customer-name="Acme Corp" \
  --interconnect-type=DEDICATED --link-type=LINK_TYPE_ETHERNET_10G_LR --requested-link-count=1 \
  --location=iad-zone1-1 --admin-enabled --noc-contact-email=noc@example.com
```
After your resources are allocated Google emails the **LOA-CFA** (Letter of Authorization and Connecting Facility Assignment, one PDF per connection) to you and the NOC contact; it can also be retrieved from the Google Cloud console. If you do not send it to your vendor, the connection is not installed.

## 3. Cross-connect
Give the LOA-CFA to the colocation provider and order the cross-connect from your router port to Google's
demarc port (single-mode fiber: 10GBASE-LR, 100GBASE-LR4 or 400GBASE-LR4; maximum supported fibre length for these optics is 10 km).

## 4. Testing and activation
Google starts testing light levels on each allocated port after 24 hours; if they are in range it emails configuration details for a connectivity test, which you apply to your router. The interconnect `state` is `UNPROVISIONED` until turn-up completes, then `ACTIVE` (or `UNDER_MAINTENANCE`).
Watch `gcloud compute interconnects describe ic-ash-1 --format='value(state,operationalStatus)'` and optics `gcloud compute interconnects get-diagnostics ic-ash-1`.

## 5. VLAN attachments and BGP
```bash
gcloud compute interconnects attachments dedicated create va-ash-1 --region=us-east4 \
  --router=ic-router-east4 --interconnect=ic-ash-1 --vlan=100 --bandwidth=10g --mtu=8896
```
Then configure the on-prem 802.1Q subinterface and BGP to the Cloud Router IPs from `attachments describe`.

## Gotchas
- LACP is required even if you use a single circuit; the other technical requirements are IPv4 link-local addressing, EBGP-4 with multi-hop and 802.1Q VLANs.
- If light levels are out of range Google emails a failure notice; check optics and fibre.
- Plan IP and ASN details for all attachments before the circuits arrive.

## Verify
- [ ] Interconnect ACTIVE, diagnostics show good Rx/Tx light, BGP sessions up on all attachments, and routes exchanged.

## Checked

- Date: 2026-10-27; documentation release: Google Cloud documentation pages as published on that date.
- Found wrong: `--bandwidth=BPS_10G` (gcloud accepts 10g); the bundle size was given as up to 2 x 100G whereas the overview and quotas pages allow up to 8 circuits of 10, 100 or 400 Gbps; `PENDING_CUSTOMER` is not an Interconnect state (Compute API enum is ACTIVE and UNPROVISIONED, plus UNDER_MAINTENANCE in the description); the cancellation claim and the LOA 'within days' timing were not in documentation.
- Confirmed (99.99% tutorial): multi-region requirements of four connections in two metros using both edge availability domains. Confirmed (dedicated overview): optics 10GBASE-LR, 100GBASE-LR4, 400GBASE-LR4, 10 km limit, LACP even for a single circuit, 99.9% and 99.99% levels.
- Confirmed (provisioning overview and retrieving LOA pages): LOA-CFA emailed per connection, light-level testing starts after 24 hours, then connectivity-test configuration email.
- Confirmed (gcloud reference): `interconnects create` flags, `get-diagnostics`, `locations list`, `attachments dedicated create --vlan --bandwidth --mtu`.

Method: documentation only; no commands were run.
