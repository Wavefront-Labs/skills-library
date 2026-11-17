---
id: computing-software.cloud-infrastructure-engineering.google-cloud.interconnect-and-vpn-egress-pricing
name: interconnect-and-vpn-egress-pricing
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, network-service-tiers, interconnect-egress-pricing, vpn-pricing, data-transfer-cost, hybrid-connectivity]
level: practitioner
status: draft
description: "Estimate hybrid connectivity cost: Interconnect port and VLAN attachment fees, reduced Interconnect egress, HA VPN tunnel hours, and break-even vs internet egress."
sources: ["https://cloud.google.com/network-connectivity/docs/interconnect/pricing", "https://cloud.google.com/network-connectivity/docs/vpn/pricing", "https://cloud.google.com/vpc/network-pricing"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Interconnect and VPN egress pricing

## Components
| Option | Fixed | Variable |
|---|---|---|
| Dedicated Interconnect | per-port hourly (10G/100G), VLAN attachment hourly | egress from GCP over Interconnect at reduced per-GiB rate (by region/continent) |
| Partner Interconnect | VLAN attachment hourly by capacity + partner's fees | same reduced egress rate |
| Cross-Cloud Interconnect | port hourly | reduced egress |
| HA VPN | per-tunnel hourly | egress at standard internet egress rates (traffic leaves via internet) |
Ingress to Google is free for all.

## Estimating
```
monthly = ports x port_hourly x 730 + attachments x attach_hourly x 730
        + egress_GiB x interconnect_rate(src_region, dest_continent)
```
Compare with VPN: tunnels x tunnel_hourly x 730 + egress_GiB x internet_egress_rate. With a few
TB/month egress, Interconnect usually breaks even (per-GiB difference is large); check current
pricing pages, rates change.

## Measuring actual egress
Billing export SKUs contain "Interconnect" / "VPN" / "Network Egress via Carrier Peering"; query:
```sql
SELECT sku.description, SUM(usage.amount_in_pricing_units) gib, SUM(cost) cost
FROM `<P>.billing.gcp_billing_export_resource_v1_<ID>`
WHERE service.description = "Networking" AND (sku.description LIKE "%Interconnect%" OR sku.description LIKE "%VPN%")
  AND invoice.month = "202609" GROUP BY 1 ORDER BY cost DESC;
```
Interconnect attachment metrics `interconnect/network/attachment/sent_bytes_count` give per-attachment volume.

## Gotchas
- Egress via Interconnect from a region on another continent than the Interconnect location costs more (inter-region + interconnect rate).
- Partner fees (port, cross-connect, colo) are outside GCP billing.
- Redundant connections double fixed cost; required for SLA.

## Verify
- [ ] Monthly estimate reconciles with billing export within 10% after one month.
