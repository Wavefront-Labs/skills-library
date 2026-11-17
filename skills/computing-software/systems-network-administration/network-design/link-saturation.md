---
id: computing-software.systems-network-administration.network-design.link-saturation
name: link-saturation
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, troubleshooting-performance, link-saturation, congestion, output-drops, top-talkers]
level: practitioner
status: docs-checked
description: "Identify and relieve a saturated link: confirm with counters and drops, find top talkers with NetFlow, decide between QoS, rate limiting, rescheduling or upgrading."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/simple-network-management-protocol-snmp/8141-calculate-bandwidth-snmp.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/fnetflow/configuration/xe-16/fnf-xe-16-book.html
  - https://www.ntop.org/products/traffic-analysis/ntop/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Link saturation

## Confirm
- Utilisation near 100 % in one direction on SNMP graphs (1-minute polling if possible) and
  **output drops / queue drops** increasing:
  interface rate and drop counters, and per-class QoS policy statistics.
- Users see latency spikes, VoIP choppiness, slow transfers at the same times.
- Check both directions: download saturation shows on the ISP side of your edge (your inbound).

## Find who
- NetFlow/IPFIX/sFlow top talkers by source, destination, application in the saturated window
  (for example ntopng, which gathers NetFlow/sFlow from routers and switches via nProbe).
- Firewall application reports and user mapping.
- Quick look on Linux: `iftop`, `nload`; on routers, the flow cache or flow monitor output (Cisco Flexible NetFlow).
Typical culprits: backups/replication during business hours, OS/app updates, cloud sync, video
streaming, a single host with malware or misconfigured job.

## Relieve
| Action | When |
|---|---|
| QoS: protect real-time and business classes, scavenger for bulk | always, as first line |
| Shape at the edge slightly below circuit rate | so queuing happens where your QoS applies (ISP-facing) |
| Reschedule bulk jobs, throttle backup/replication bandwidth | identifiable jobs |
| Caching/peer delivery for updates  | update storms |
| Rate-limit or block abusive flows | non-business usage |
| Upgrade capacity / add a second link with load balancing (SD-WAN) | sustained high 95th percentile utilisation |

## Verify
- [ ] After the fix, drops in priority classes are zero, 95th percentile utilisation is below threshold, and user-facing latency returns to baseline.

## Checked

- Date: 2026-10-28
- Confirmed: ntop page: ntopng with nProbe collects NetFlow/sFlow; Cisco SNMP bandwidth document and Flexible NetFlow guide exist as cited background.
- Removed: exact IOS commands, tool name lists, update-cache product names, 70 % threshold.
Method: documentation only; no commands were run.
