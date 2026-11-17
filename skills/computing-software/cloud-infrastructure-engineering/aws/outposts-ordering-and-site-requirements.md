---
id: computing-software.cloud-infrastructure-engineering.aws.outposts-ordering-and-site-requirements
name: outposts-ordering-and-site-requirements
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, outposts, outposts-ordering, site-requirements, outposts-rack, service-link, hybrid-infrastructure]
level: practitioner
status: docs-checked
description: "Order AWS Outposts correctly: rack vs server form factors, site requirements (power, cooling, network uplinks, service link), catalog items, order API, and installation steps."
sources: ["https://docs.aws.amazon.com/outposts/latest/userguide/outposts-requirements.html", "https://docs.aws.amazon.com/outposts/latest/userguide/order-outpost-capacity.html", "https://docs.aws.amazon.com/outposts/latest/userguide/what-is-outposts.html", "https://docs.aws.amazon.com/outposts/latest/userguide/region-connectivity.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Outposts ordering and site requirements

## Form factors
| | Outposts rack | Outposts servers |
|---|---|---|
| Size | industry-standard 42U rack (80 in high, 24 in wide, 48 in deep) with rack-mountable servers, switches, patch panel and power shelf | industry-standard 1U or 2U server for a 19-inch EIA-310D 4-post rack |
| Services | supported services depend on the Region of the Outpost; see the supported-services list | see the Outposts servers guide |
| Use | data centres needing local AWS at scale | small footprints |
Servers have their own site requirements (Outposts servers guide). The rest of this skill covers racks.

## Site requirements (racks, summarised; read the full checklist)
- **Power:** the API offers 5, 10, 15 and 30 kVA draw (`POWER_5_KVA` ... `POWER_30_KVA`), single or three phase, with listed connectors (for example L6-30P or IEC309) and feed drops from the two power sources.
- **Cooling and environment:** racks draw cold air from the front aisle and exhaust to the back aisle; the rack position must provide airflow of at least 145.8 times the kVA in CFM; elevation below 3,050 m (10,005 ft).
- **Space and weight:** doorways, hallways, turns and ramps must clear the 80 x 24 x 48 inch rack; check floor loading and seismic anchorage with a structural engineer.
- **Network:** uplinks of 1, 10, 40 or 100 Gbps (`UPLINK_1G`, `UPLINK_10G`, `UPLINK_40G`, `UPLINK_100G`) over single-mode or multi-mode fiber with listed optics; LACP (dynamic LAG) is required between the Outpost and your network; each of the two network devices needs a /30 or /31 CIDR for the **service link** and for the **local gateway**, plus BGP peer IP and ASN (2- or 4-byte).
- **Service link** to the parent Region: see the service-link connectivity page for MTU, 175 ms latency and bandwidth recommendations.

## Order flow
```bash
aws outposts create-site --name lyon-dc1 --operating-address file://address.json \
  --rack-physical-properties PowerDrawKva=POWER_10_KVA,PowerPhase=THREE_PHASE,UplinkGbps=UPLINK_10G,UplinkCount=UPLINK_COUNT_2,FiberOpticCableType=SINGLE_MODE
aws outposts create-outpost --name lyon-outpost --site-id "$SITE" --availability-zone eu-west-3a
aws outposts list-catalog-items --query 'CatalogItems[].[CatalogItemId,EC2Capacities,PowerKva]'
aws outposts create-order --outpost-identifier "$OUTPOST" \
  --line-items CatalogItemId=OR-XXXX,Quantity=1 --payment-option ALL_UPFRONT --payment-term THREE_YEARS
```
- Payment terms are `ONE_YEAR`, `THREE_YEARS` or `FIVE_YEARS`, with `ALL_UPFRONT`, `PARTIAL_UPFRONT` or `NO_UPFRONT` (monthly charges over the term if not all upfront). Choose renewal options at least 5 business days before the subscription ends. Capacity is chosen from catalog items; a quote can be generated before ordering.
- You provide site details (operating and shipping address, rack physical properties) and network configuration (CIDRs, IPs, BGP ASNs).

## After install
- Create subnets on the Outpost (`create-subnet --outpost-arn`).

## Verify
- [ ] Site checklist signed off by facilities (power, cooling, network) before ordering.
- [ ] Service link redundancy tested; first instances launched on the Outpost subnet.

## Checked

2026-10-28. Confirmed against the Outposts rack User Guide pages (site requirements, create order, what is Outposts, service link connectivity) and the outposts botocore model: form factors, rack dimensions, airflow, elevation, LACP requirement, uplink speeds and fiber types, /30 or /31 service link and local gateway CIDRs, BGP, 175 ms service link latency mention, payment options and terms, 5-business-day renewal notice, create-site/create-order shapes. Removed (unconfirmed): list of rack services, servers service set, "some operations fail when service link is down", CloudWatch namespace, local gateway route table advice, Direct Connect/VPN wording. Read end to end.

Method: documentation only; no commands were run.
