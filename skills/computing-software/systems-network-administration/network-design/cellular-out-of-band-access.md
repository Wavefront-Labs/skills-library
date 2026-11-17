---
id: computing-software.systems-network-administration.network-design.cellular-out-of-band-access
name: cellular-out-of-band-access
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, access-management, cellular-oob, out-of-band, console-server, lte-oob]
level: practitioner
status: docs-checked
description: "Add cellular out-of-band access to remote sites: console servers with LTE/5G, private APN vs VPN, security, power, and testing that OOB works before you need it."
sources:
  - https://opengear.com/products/
  - https://www.zpesystems.com/products/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Cellular out-of-band access

## Why
When a change breaks the WAN, or the router/firewall dies, the only way in is OOB. Cellular OOB
has an independent path from the production circuit, avoiding a truck roll.

## Components
- Console server with a built-in LTE/5G modem, serial ports to every network device console, plus
  USB console.
- Optional: managed PDU for remote power cycling, environmental sensors.
- Out-of-band Ethernet to device management ports where available.

## Connectivity models
| Model | Notes |
|---|---|
| Private APN from the carrier | SIMs get private IPs reachable from your DC only; no internet exposure |
| Public SIM + outbound VPN (IPsec/WireGuard) to a hub | console server initiates; works behind CGNAT |
| Vendor cloud management | central access, enrolment, firmware |
Never expose console servers' SSH directly on public cellular IPs.

## Security
- AAA (TACACS+/RADIUS) with local fallback, MFA via the central access hub, per-port access control.
- Serial session logging.
- Data plan with alerts for unexpected usage.

## Operational
- Antenna placement: test signal in the comms room; external antenna if RSSI weak.
- Power from UPS on a separate circuit from the router where possible.
- **Monthly automated test**: connect over OOB, run a console command on each port, alert on
  failure. Untested OOB fails when needed.

## Verify
- [ ] With the production WAN shut down in a test window, an engineer reaches every device console at the site via cellular within the agreed recovery time.

## Checked

2026-10-28: The Opengear and ZPE pages returned only product listings and the Cisco datasheet URL is a 404, so no figures or product claims were confirmed. Removed the vendor and product names (Opengear, ZPE Nodegrid, Lantronix, Cisco terminal server gateway, Perle, Lighthouse, ZPE Cloud) and the 5 minute test target. The connectivity models and the monthly test are process guidance.
Method: documentation only; no commands were run.
