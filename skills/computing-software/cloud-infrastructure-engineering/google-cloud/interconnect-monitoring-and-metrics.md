---
id: computing-software.cloud-infrastructure-engineering.google-cloud.interconnect-monitoring-and-metrics
name: interconnect-monitoring-and-metrics
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, hybrid-connectivity, interconnect-monitoring, interconnect-metrics, bgp, alerting]
level: advanced
status: docs-checked
description: "Monitor Cloud Interconnect: link up/down, receive and transmit light levels, VLAN attachment throughput and drops, BGP session state and learned-route alerts."
sources: ["https://cloud.google.com/network-connectivity/docs/interconnect/how-to/monitoring", "https://cloud.google.com/monitoring/api/metrics_gcp_i_o", "https://cloud.google.com/monitoring/api/metrics_gcp_p_z"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Interconnect monitoring

Cloud Interconnect reports to Cloud Monitoring in one-minute intervals, retained for 6 weeks. Dedicated Interconnect reports both the connection (physical circuit) and the VLAN attachments; Partner Interconnect reports VLAN attachments only. Connection metrics start as soon as Google allocates your ports, before the circuit is ready, so you can watch it while it is built and tested.

## 1. Metrics (`interconnect.googleapis.com/...`)
| Metric | Watch |
|---|---|
| `network/interconnect/link/operational` | BOOL per physical circuit (`link_id`); false = circuit down |
| `network/interconnect/operational` | BOOL for the whole LACP bundle |
| `network/interconnect/link/rx_power`, `tx_power` | light level in dBm per circuit and laser; drift = dirty or failing optic |
| `network/interconnect/capacity`, `network/attachment/capacity` | provisioned capacity (By/s) |
| `network/attachment/received_bytes_count`, `sent_bytes_count` | utilisation per VLAN attachment |
| `network/attachment/ingress_dropped_packets_count`, `egress_dropped_packets_count` | dropped packets per attachment (label `drop_reason`) |
| `network/interconnect/dropped_packets_count` | outbound packets dropped due to link congestion |
| Cloud Router `router.googleapis.com/bgp/session_up` | 1 = session up, 0 = down, label `bgp_peer_name` |
| `router.googleapis.com/bgp/received_routes_count` | routes received per session; a sudden drop means the peer withdrew routes |

## 2. Alerts (example thresholds, tune to your design)
- Link operational false for 1 minute (page).
- BGP `session_up` == 0 for 2 minutes per peer.
- Attachment utilisation above 80% of capacity for 15 minutes: `sent_bytes_count` rate x 8 / `attachment/capacity`.
- Dropped packets above 0, sustained.
- `rx_power` trending down toward your optic's low-warning level (take the level from the optic's data sheet or Google's circuit diagnostics).
Create them under Monitoring > Alerting with the resource type Interconnect and metric category Network.

## 3. Diagnostics
```bash
gcloud compute interconnects get-diagnostics ic-ash-1
```
The console also shows a Monitoring tab on each connection (utilisation against capacity, bytes by VLAN attachment, drops and errors) and each VLAN attachment, and Network Topology overlays throughput per connection. Before planned maintenance, confirm routes fail over to the redundant path.

## Gotchas
- Utilisation must be evaluated per attachment (VLAN), not just per physical link: an attachment with a smaller capacity drops traffic while the link looks idle.
- BGP up with zero learned routes is a silent outage; alert on `received_routes_count` too.

## Verify
- [ ] Dashboard has per-link status/light and per-attachment utilisation; disabling one BGP peer in a test window fires the alert and traffic shifts to the other path.

## Checked
2026-10-31. Confirmed against the Cloud Interconnect "Monitor connections" page and the Cloud Monitoring metrics list (interconnect and router/vpn sections): every metric name, type, label and the 1-minute interval and 6-week retention; `get-diagnostics` against the gcloud reference. Removed: maintenance-notification email routing, the 99.99% maintenance claim and the per-link "LACP, ARP" diagnostics detail (the diagnostics page returned a redirect and could not be read); alert thresholds are labelled as examples, not documented values.
Method: documentation only; no commands were run.
