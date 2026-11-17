---
id: computing-software.systems-network-administration.dns-dhcp.rogue-dhcp-server-detection
name: rogue-dhcp-server-detection
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, dhcp-troubleshooting, rogue-dhcp, rogue-dhcp-detection, dhcp-snooping, dhcp-server-identifier, nmap-broadcast-dhcp-discover, dhcp-offer, windows-dhcp-authorization, home-router, wrong-gateway]
level: practitioner
status: draft
description: "Find and stop a rogue DHCP server: symptoms, server ID in leases and OFFER captures, nmap broadcast discovery, tracing its MAC to a port, DHCP snooping."
sources:
  - https://nmap.org/nsedoc/scripts/broadcast-dhcp-discover.html
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/sec/b_179_sec_9300_cg/configuring_dhcp.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rogue DHCP server detection

## Symptoms
Clients in one VLAN get addresses from the wrong range (192.168.0.x/192.168.1.x from a home
router plugged in by a user), wrong gateway or DNS, intermittent internet, captive-portal-like
behaviour (malicious rogue).

## Identify the server
1. On an affected client:
   - Windows `ipconfig /all`: **DHCP Server** address.
   - Linux: `journalctl -u NetworkManager | grep -i dhcp`, or `cat /var/lib/dhcp/dhclient*.leases`
     (`option dhcp-server-identifier`).
2. Capture OFFERs: `sudo tcpdump -ni eth0 -vvv 'udp port 67 or 68'` then release/renew; or
   Wireshark filter `dhcp.option.dhcp == 2` (OFFER) and look at `dhcp.option.dhcp_server_id` and
   the Ethernet source MAC. More than one server ID answering = rogue present.
3. Active probe: `sudo nmap --script broadcast-dhcp-discover -e eth0` sends a DHCP request to
   the broadcast address and reports the responses. By default it uses a static client MAC
   (DE:AD:C0:DE:CA:FE) to prevent IP pool exhaustion; setting `broadcast-dhcp-discover.mac=random`
   may make the server reserve a new address each time. Needs root; default timeout is 10 s.
4. The OFFER's source MAC: find it on the switch with `show mac address-table address <mac>` and
   follow to the access port (trace-host-to-switch-port). OUI often reveals a consumer router.

## Stop it
- Shut the port, remove the device, talk to the user.
- Release/renew affected clients (`ipconfig /release && ipconfig /renew`, `dhclient -r && dhclient`).

## Prevent
- **DHCP snooping** on access switches: only trusted ports (uplinks, legitimate servers) may send
  OFFER/ACK; others dropped and logged.
  ```
  ip dhcp snooping
  ip dhcp snooping vlan 10,20
  no ip dhcp snooping information option     ! if your server rejects option 82 from the switch
  interface Te1/1/1
   ip dhcp snooping trust
  ```
- Windows DHCP: only servers **authorised in AD** start serving (protects against stray Windows
  servers, not routers).
- Wireless: client isolation and controller DHCP-required/rogue DHCP detection features.
- NAC/802.1X keeps unknown devices off production VLANs.

## Verify
- [ ] broadcast-dhcp-discover returns only the legitimate server(s) on each VLAN.
- [ ] DHCP snooping drop counters/logs alert on untrusted OFFERs.
