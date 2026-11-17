---
id: computing-software.digital-privacy-hygiene.device-hardening.router-admin-lockdown-and-upnp
name: router-admin-lockdown-and-upnp
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, router-admin-password, upnp, router-security, home-network, remote-management, wps, port-forwarding, isp-router, cisa-home-network, port-forwarding-review]
level: practitioner
status: draft
description: "Lock down a home router's admin side: unique admin password, remote management off, UPnP and WPS off, review port forwards, and check for ISP-managed access."
sources:
  - "https://www.cisa.gov/news-events/news/home-network-security"
  - "https://www.cisa.gov/secure-our-world/secure-your-home-wi-fi"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Router admin lockdown and UPnP

**Goal:** the router is the front door of every device at home. Compromised consumer
routers are routinely used in botnets and for DNS hijacking.

## Admin access
1. Log in to the admin page (address on the router label, e.g. `192.168.1.1`, or the
   vendor app).
2. Change the **admin password** from the default/label password to a unique generated one
   (stored in the vault). This is separate from the Wi-Fi password.
3. **Remote management / WAN administration**: off (unless you need it; then restrict to
   your IP or use the vendor's cloud app with MFA).
4. Firmware: update now, enable automatic updates (see router firmware coverage in
   `computing-software.digital-privacy-hygiene.device-hardening.personal-device-hardening-checklist`).

## UPnP and WPS
- **UPnP**: lets any device on the LAN open inbound ports automatically. Malware and
  insecure IoT abuse it. Turn **off**; add manual port forwards for the few things that
  need them (game consoles may complain of "strict NAT"; accept or forward specific ports).
- **WPS** (push-button/PIN pairing): PIN mode is brute-forceable; turn off.

## Review
- **Port forwarding** list: delete anything you don't recognise.
- **Connected devices**: identify unknowns; change Wi-Fi password if needed.
- **DNS settings**: confirm they're yours (DNS hijack malware changes them).
- ISP-provided routers may have ISP remote access (TR-069) you can't disable; consider your
  own router behind it.

## Verify
- [ ] Admin password changed, remote admin off, UPnP and WPS off, port forwards justified.
