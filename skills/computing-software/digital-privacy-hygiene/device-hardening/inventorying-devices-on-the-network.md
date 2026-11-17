---
id: computing-software.digital-privacy-hygiene.device-hardening.inventorying-devices-on-the-network
name: inventorying-devices-on-the-network
category: computing-software
field: digital-privacy-hygiene
product: device-hardening
tags: [digital-privacy-hygiene, device-hardening, network-device-inventory, home-network, nmap, router-client-list]
level: practitioner
status: draft
description: "List every device on your home network from the router, Fing or nmap, identify unknowns despite MAC randomisation, and remove intruders."
sources:
  - "https://nmap.org/book/man-host-discovery.html"
  - "https://www.cisa.gov/news-events/news/home-network-security"
  - "https://www.fing.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Inventorying devices on the network

**Goal:** know what's connected, so an unknown device stands out.

## Sources
1. **Router admin page** or app: "Connected devices" / DHCP client list with name, MAC, IP, band.
2. **Fing** (mobile/desktop) scans and identifies device types.
3. **nmap** from a computer:
   ```
   nmap -sn 192.168.1.0/24          # ping scan; lists live hosts with MAC vendor when run as root
   arp -a                           # what this computer has seen
   ```

## Identify each
- Vendor from the MAC prefix (OUI). Phones and laptops use **randomised private MACs** per network, so the vendor may
  show as unknown; match by hostname, by switching devices off one at a time, or by checking the device's Wi-Fi
  details for its MAC on this network.
- Rename devices in the router so the list is readable ("Kitchen speaker").
- Keep a simple table: device, owner, MAC, IP reservation, network (main/IoT/guest).

## Unknown device?
1. Block it in the router (MAC block is only a stopgap).
2. Change the Wi-Fi password (WPA3 or WPA2-AES), disable WPS, and rejoin your own devices.
3. Check for a neighbour on an old shared password or a forgotten device first.

## Habit
Check monthly and after guests. Put IoT and guests on separate networks so the main list stays short.
