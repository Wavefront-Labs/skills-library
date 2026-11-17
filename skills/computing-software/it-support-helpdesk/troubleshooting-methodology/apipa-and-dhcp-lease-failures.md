---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.apipa-and-dhcp-lease-failures
name: apipa-and-dhcp-lease-failures
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, networking, network-troubleshooting, apipa, 169-254, dhcp, dhcp-lease, ipconfig-renew, dhcp-scope-exhausted, comptia-a-plus, limited-connectivity]
level: intro
status: draft
description: "Diagnose a 169.254.x.x (APIPA) address or no DHCP lease: physical link, VLAN/port, DHCP scope exhaustion, relay/helper, 802.1X blocks, and the client-side renew sequence."
sources:
  - "https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/troubleshoot-dhcp-guidance"
  - "https://www.rfc-editor.org/rfc/rfc3927"
  - "https://www.comptia.org/certifications/a"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# apipa-and-dhcp-lease-failures

Goal: when a PC shows "No internet" with a 169.254.x.x address, find why it
got no lease (A+ 220-1201 5.7: limited/no connectivity, APIPA).

## Read the client
```cmd
ipconfig /all
```
- IPv4 `169.254.x.x` (Autoconfiguration IPv4 Address) = DHCP request got
  no answer (RFC 3927 link-local).
- "Media disconnected" = no link at all → physical layer.
- DHCP Enabled: No with a static address = someone set it manually.

## Client-side sequence
```cmd
ipconfig /release
ipconfig /renew
```
- Renew error "unable to contact your DHCP server" → no reply.
- Disable/enable the adapter; check driver (Device Manager).
- Wi-Fi: forget and rejoin the network.

## Ladder
1. **Link**: cable/port lights, try another port/cable, dock vs direct.
2. **Is it just this device?** Another device on the same port/SSID gets
   an address → client problem (driver, firewall/security agent, 802.1X).
   None do → network side.
3. **802.1X / NAC**: port or SSID requires authentication; failed auth may
   leave the device with no VLAN → APIPA. Check the security agent/NAC
   portal, certificates.
4. **DHCP scope exhausted**: busy guest Wi-Fi, long lease times — DHCP
   server shows scope 100 % used; shorten leases, expand scope, clear stale
   leases.
5. **Relay**: client VLAN needs an IP helper/DHCP relay to reach the server
   — new VLAN without helper = nobody gets addresses.
6. **DHCP server/service down** or unauthorised (rogue DHCP handing wrong
   addresses is a different symptom: wrong subnet/gateway, not APIPA).

## Gotchas
- A PC with a valid address but wrong subnet (e.g. 192.168.1.x on a
  corporate 10.x network) = rogue DHCP (home router plugged into the LAN).
- Some docks/USB NICs need their own driver; built-in NIC works, dock NIC
  doesn't.
- Static IP left from a previous site → set back to automatic.

## Verify
`ipconfig /all` shows a lease from the expected DHCP server with correct
gateway and DNS; `ping` gateway and `nslookup` an internal name succeed.
