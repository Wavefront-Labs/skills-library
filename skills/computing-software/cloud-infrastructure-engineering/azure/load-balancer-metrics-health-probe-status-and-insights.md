---
id: computing-software.cloud-infrastructure-engineering.azure.load-balancer-metrics-health-probe-status-and-insights
name: load-balancer-metrics-health-probe-status-and-insights
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, load-balancer, lb-insights, health-probe-status, lb-metrics, data-path-availability, snat-ports]
level: practitioner
status: docs-checked
description: "Monitor Standard Load Balancer: data path availability, health probe status per backend, SNAT metrics, LB Insights and alerts that catch a dying backend pool."
sources: ["https://learn.microsoft.com/azure/load-balancer/load-balancer-standard-diagnostics", "https://learn.microsoft.com/azure/load-balancer/load-balancer-insights", "https://learn.microsoft.com/azure/load-balancer/load-balancer-troubleshoot-health-probe-status"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Load balancer metrics, probe status and insights

**Goal:** know immediately when backends fail probes or the frontend data path degrades.

## Key metrics (Standard SKU only; Basic has no multi-dimensional metrics)
| Metric | Meaning | Recommended aggregation |
|---|---|---|
| Data Path Availability | Synthetic probe through the frontend to the host of a backend VM; filter by frontend IP and port | Average |
| Health Probe Status | How the LB sees each backend per your probe config; view per instance (backend IP and port) | Average |
| SNAT Connection Count | Outbound flows, successful and failed; filter Connection State = Failed (public LB) | Sum |
| Allocated / Used SNAT Ports | Port allocation and pressure per backend instance (public LB) | Average |
| Byte / Packet / SYN Count | Traffic per frontend | Sum |

Metrics are sampled once per minute, so use a time aggregation above one minute for Sum and Count. Data Path Availability can take up to 10 minutes to appear after a load balancer is created or updated, and it is not generated for empty backend pools or frontends without load-balancing rules. Pull metrics programmatically through the Azure Monitor REST API, or write them to storage with a diagnostic setting for the All Metrics category.

## Alerts
- Health Probe Status (Average), split by backend IP address and port: one alert per instance. The Learn guidance is Average over a five-minute look-back with a 95% threshold to avoid noisy alerts.
- Data Path Availability, split by frontend IP and frontend port, less than or equal to 0 fires when any load-balancing rule becomes unresponsive.
- SNAT Connection Count with Connection State = Failed, Total aggregation, split by backend IP, greater than 0 means outbound port exhaustion (use NAT Gateway for more SNAT capacity).
- Used SNAT Ports, Average, split by backend IP and protocol: for example low severity at 75% of allocated ports and high severity at 90% or 100%.

## Resource Health
Standard LB Resource Health (Monitor > Service health) is evaluated every two minutes from Data Path Availability: Degraded means under 90% but over 25% for at least two minutes, Unavailable means under 25%.

## Insights and health views
- Azure Monitor > Networks > Load balancers (LB Insights): functional dependency view with backend pools colour-coded by Health Probe Status, plus *More Detailed Metrics*, a preconfigured workbook with Overview, Frontend and Backend Availability, Data Throughput, Flow Distribution, Connection Monitors and Metric Definitions tabs.
- A backend you intentionally probe down (active/passive) shows red in Insights; that is expected.
- The topology comes from Azure Resource Graph, so configuration changes can take up to 30 hours to appear.

## Probe-down checklist
1. Probe port/path served by the app on every instance (`curl http://localhost:<port><path>` on the VM).
2. NSG allows source **AzureLoadBalancer** service tag (168.63.129.16) to the probe port.
3. Guest firewall (Windows Firewall/iptables) allows it.
4. HTTP probe expects **200** - any other response code (for example 403, 404, 500) counts as down.
5. Probe interval/threshold vs app restart times.

## Gotchas
- Basic LB is retired and has no multi-dimensional metrics - upgrade.
- Health Probe Status dips during deployments are expected; set alert windows accordingly.
- Deallocated VMs aren't probed and stop reporting metrics; the portal shows a dashed line.
- If the backend pool is empty, Data Path Availability alerts never fire.

## Verify
- [ ] Stopping the app on one VM triggers the per-backend alert within minutes; metrics dashboard pinned for the service.

## Checked

2026-10-31. Confirmed against the Learn Standard Load Balancer diagnostics page (metric names, aggregation guidance, one-minute sampling, 10-minute appearance delay, alert examples, SNAT thresholds, Resource Health states and thresholds, deallocated VM behaviour), the Load Balancer Insights page (dependency view, workbook tabs, 30-hour Resource Graph delay, red indicator for intentional probe down) and the custom probe overview (non-200 responses count as down, AzureLoadBalancer tag and 168.63.129.16). Removed: the VipAvailability and DipAvailability metric IDs, the az monitor metrics command that used them, the 100 and 50 and 90-for-5-minutes thresholds, the 401 remark and the split-by column details not stated in the docs.

Method: documentation only; no commands were run.
