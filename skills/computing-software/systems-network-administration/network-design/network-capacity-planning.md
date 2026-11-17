---
id: computing-software.systems-network-administration.network-design.network-capacity-planning
name: network-capacity-planning
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, documentation, network-capacity-planning, trend-analysis, forecasting, utilisation]
level: practitioner
status: draft
description: "Plan network capacity from data: collect 95th percentile utilisation, forecast growth by trend and business events, set upgrade thresholds and lead times."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/simple-network-management-protocol-snmp/8141-calculate-bandwidth-snmp.html
  - https://grafana.com/docs/grafana/latest/panels-visualizations/query-transform-data/transform-data/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network capacity planning

## Data to collect
- Interface utilisation (bps in/out) at 1-5 minute resolution, kept for 13+ months: WAN, internet,
  uplinks, inter-DC, firewall throughput.
- Drops/discards and queue drops per class.
- Device resources: CPU, memory, TCAM, MAC/ARP/route table sizes, firewall sessions/connections per
  second, VPN tunnel counts, DHCP scope usage, wireless clients per AP, PoE budget.

## Analysis
1. Reduce to **monthly 95th percentile** per link and direction (removes rare spikes, keeps sustained
   peaks).
2. Fit a trend (linear or compound monthly growth) over 6-12 months.
3. Overlay known business events: office moves, new apps, M&A, seasonal peaks.
4. Compute time-to-threshold: months until 95th percentile reaches the upgrade threshold.

## Thresholds and lead time
| Resource | Upgrade trigger |
|---|---|
| WAN/internet | 95th percentile > 70 % (sooner if real-time traffic queues) |
| Campus uplinks | > 50-60 % or any sustained discards |
| Tables/sessions/TCAM | > 70-80 % of platform limit |
| Scope/pool use | > 80 % |
Trigger the upgrade **lead time + safety margin** before the forecast crosses: circuits often take
60-90 days, hardware refresh longer.

## Output
Quarterly capacity report: top N constrained resources, forecast date, proposed action, cost, owner.

## Verify
- [ ] Report covers all WAN/internet links and key device tables; no link hit its threshold without a planned upgrade already in flight.
