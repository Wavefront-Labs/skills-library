---
id: computing-software.digital-privacy-hygiene.device-hardening.isp-router-bridge-mode
name: isp-router-bridge-mode
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, bridge-mode, home-network, isp-router, double-nat]
level: practitioner
status: draft
description: "Put an ISP-supplied router into bridge or modem mode (or IP passthrough) so your own router does security, and avoid double NAT and ISP Wi-Fi."
sources:
  - "https://www.cisa.gov/news-events/news/home-network-security"
  - "https://openwrt.org/docs/guide-user/network/wan/isp-configurations"
  - "https://www.nsa.gov/Press-Room/Cybersecurity-Advisories-Guidance/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# ISP router limits and bridge mode

**Goal:** a router you control (updated firmware, your settings) is the one facing the internet.

## Why
ISP routers often lag on firmware, have limited settings, keep remote management (TR-069) for the ISP, and broadcast
their own Wi-Fi. Running your own router behind one also creates **double NAT**, which breaks gaming, VPN servers and
port forwarding.

## Options
| Mode | What happens |
|---|---|
| **Bridge / modem mode** | ISP box only converts the line; your router gets the public IP |
| **IP passthrough** (common on fibre/AT&T style gateways) | Box still routes but hands its public IP to your router |
| **DMZ to your router** | Fallback when no bridge option; still double NAT for some things |

Find it in the ISP router admin page (often under WAN, Internet, Modem mode) or ask support. Some ISPs need a call.

## Check
On your router's status page, the WAN IP should be public. If it's `192.168.x.x`, `10.x.x.x`, `172.16-31.x.x`, you're
double-NATed; `100.64-127.x.x` means carrier-grade NAT from the ISP (bridge mode won't fix that).

## After
- Turn off the ISP box's Wi-Fi (bridge mode does this automatically on most).
- Secure your own router: admin password, updates, WPA3, UPnP off.
- Phone (VoIP) and TV services may depend on the ISP box; check they still work or use passthrough instead.

## Gotchas
- Fibre ONTs and some cable modems can't be replaced; the ISP still manages them.
- Factory reset of the ISP box can undo bridge mode.
