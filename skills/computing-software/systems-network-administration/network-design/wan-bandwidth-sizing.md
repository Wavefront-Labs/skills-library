---
id: computing-software.systems-network-administration.network-design.wan-bandwidth-sizing
name: wan-bandwidth-sizing
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, wan-sizing, bandwidth-planning, wan-design, voice-bandwidth, capacity-planning]
level: practitioner
status: draft
description: "Size WAN and internet circuits: per-user and per-app baselines, voice/video call bandwidth, peak vs average, measured 95th percentile, headroom and growth."
sources:
  - https://www.cisco.com/c/en/us/support/docs/voice/voice-quality/7934-bwidth-consume.html
  - https://learn.microsoft.com/en-us/microsoftteams/prepare-network
  - https://support.zoom.com/hc/en/article?id=zm_kb&sysparm_article=KB0060748
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# WAN bandwidth sizing

## Inputs
1. **Measured data** if the site exists: NetFlow/IPFIX top talkers and 95th percentile utilisation
   over a month on the current circuit (not 5-minute peaks, not averages).
2. **Users and apps** for new sites: concurrent users x per-user demand by app.
3. **Real-time traffic** sized separately.

## Real-time per-call bandwidth (per direction, incl. IP/UDP/RTP + L2)
| Codec / app | Bandwidth |
|---|---|
| G.711 20 ms | ~87 kbps (Ethernet) |
| G.729 20 ms | ~31 kbps |
| Teams audio | 45-100 kbps |
| Teams/Zoom 1:1 HD video | 1.5-2.5 Mbps |
| Teams/Zoom gallery 1080p | 2.5-4 Mbps |
Concurrent calls ~ users x peak-hour call ratio (Erlang B for trunks; 1:4 to 1:6 for typical offices).

## Data
Rule of thumb for office SaaS users: 0.5-2 Mbps per concurrent active user at peak, higher for
CAD/media. Add backups/replication windows, OS/app updates (use caching/peer delivery), cloud
file sync.

## Formula
Required = (real-time peak) + (data 95th percentile or estimate) x growth (20-30 %/year over the
contract) / target utilisation (70-80 %).

## Also check
- Upload: video calls and cloud backup make upstream the bottleneck on asymmetric links.
- Failover link: can the backup carry the critical classes alone? Size QoS policy for that case.
- Latency matters more than bandwidth for interactive apps; more Mbps will not fix 150 ms.

## Verify
- [ ] After go-live, monthly 95th percentile < 70 % and no sustained queue drops in real-time classes.
