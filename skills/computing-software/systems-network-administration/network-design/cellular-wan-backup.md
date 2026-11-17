---
id: computing-software.systems-network-administration.network-design.cellular-wan-backup
name: cellular-wan-backup
category: computing-software
field: systems-network-administration
product: network-design
tags: [wan-design, lte-backup, cellular-wan, 5g, failover, cgnat, data-caps, branch]
level: practitioner
status: docs-checked
description: "Design LTE/5G as branch WAN backup or primary: modem and antenna placement, CGNAT and inbound access, data-cap control, and failover testing."
sources:
  - https://www.3gpp.org/technologies/lte-advanced
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cellular WAN backup

## Hardware and placement
- Integrated modem (router NIM/pluggable) or external cellular gateway on a cable run to a window or
  the roof. Basements and comms rooms in building cores have poor signal.
- Use the modem vendor's recommended antenna count (MIMO), ideally external directional/omni antennas with low-loss cable.
- Dual SIM from different carriers if the site is critical.

## Signal targets
Survey signal before committing: one floor can make a large difference. Read the modem's radio status
(signal strength RSRP, quality RSRQ and SINR) and use the modem vendor's recommended thresholds as the
target.

## IP and access realities
- Many data SIMs sit behind carrier CGNAT, which blocks inbound connections. Use outbound
  tunnels (SD-WAN, IPsec initiated from the branch, cloud management) or buy a private APN/static IP.
- Private APN can land directly in the corporate network (carrier-side VPN), avoiding the internet.
- Carrier MTU can be lower than Ethernet's; test it and clamp MSS on tunnels over cellular.

## Data caps and cost
- Keep it backup-only: floating static or SD-WAN policy marks cellular as last resort.
- Prevent background sync over cellular: block software updates, backups and cloud sync when on
  backup (SD-WAN app policies or ACLs tied to the failover track).
- Monitor usage (router counters, SIM portal alerts).

## Failover design
Track primary-WAN reachability with a probe and attach the tracked default route to it; keep a
higher-distance (floating) default route via the cellular interface as last resort.
Tunnels must re-establish over cellular (DPD/keepalives); routing over the tunnel then converges.

## Test
Pull the primary WAN cable monthly (or automate a shutdown in a window); measure time to restore
critical apps and confirm data-saving policies engage.

## Verify
- [ ] Signal metrics within the vendor's recommended range, failover under the target time, and usage alarms
  configured.

## Checked

2026-10-28: The Cisco LTE feature guide URL is a 404 and the 3GPP page returned no LTE content, so nothing was confirmed from the sources. Removed: the RSRP/RSRQ/SINR good-usable-poor table, show cellular commands, the CGNAT 100.64.0.0/10 range, the 1430-1500 MTU range, the IP SLA and track configuration with its addresses and distance 250, and the two-antenna minimum.
Method: documentation only; no commands were run.
