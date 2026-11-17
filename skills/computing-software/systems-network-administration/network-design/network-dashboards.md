---
id: computing-software.systems-network-administration.network-design.network-dashboards
name: network-dashboards
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, monitoring, network-dashboard, grafana, noc-dashboard, slo]
level: practitioner
status: docs-checked
description: "Build network dashboards people use: audience-specific views (NOC, engineering, management), the few panels that matter, Grafana layouts, and avoiding wallboard clutter."
sources:
  - https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/best-practices/
  - https://sre.google/sre-book/monitoring-distributed-systems/
  - https://docs.librenms.org/Extensions/Dashboards/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network dashboards

## One dashboard per audience
| Audience | Content |
|---|---|
| NOC wallboard | red/amber/green per site and core service, active alarms, WAN/internet status; nothing that needs reading closely |
| Engineer drill-down | per device/link: utilisation in/out, errors/discards, CPU/memory, BGP/OSPF neighbours, latency/loss probes, with template variables (site, device, interface) |
| Service view | user-centric: DNS/DHCP success rate, Wi-Fi connection success and time-to-connect, VPN users, SaaS latency |
| Management | monthly availability vs SLA, capacity forecast, incidents |

## Panels that earn their place
- The SRE book's four golden signals (latency, traffic, errors, saturation) adapted to networks: **latency, loss, utilisation, errors**, plus saturation of
  tables/sessions.
- Utilisation as % of capacity (not raw bps); show both directions.
- Synthetic probe results per site (ping/HTTP/DNS) as heatmaps.
- Annotations for changes/deploys so correlation is visible.

## Grafana practice
- Template variables for site/device/interface; repeat rows by variable.
- Consistent units across panels.
- Link panels to drill-down dashboards and runbooks.
- Keep dashboards in version control so they survive rebuilds.
- Limit each dashboard to what fits one screen; split rather than scroll.

## Verify
- [ ] During the last incident, the on-call engineer found the faulty link/site from the dashboards within minutes; unused dashboards pruned quarterly.

## Checked

- Date: 2026-10-28
- Confirmed: Grafana best practices: template variables prevent dashboard sprawl and let one dashboard serve many nodes; SRE book: dashboards normally include some form of the four golden signals.
- Removed: 70/90 % thresholds, y-axis and legend rules, provisioning claim, repeat-row claim.
Method: documentation only; no commands were run.
