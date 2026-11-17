---
id: computing-software.systems-network-administration.cisco-networking.ios-dhcp-pool-options-150-43
name: ios-dhcp-pool-options-150-43
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, dhcp, dhcp-option-43, ios-dhcp-server, wlc-discovery, vendor-class-identifier, capwap]
level: practitioner
status: docs-checked
description: "Build DHCP option 43 on an IOS DHCP pool so Cisco access points find their WLC: the f1 type-length-value hex string, option 60 matching, and how to verify."
sources:
  - https://www.cisco.com/c/en/us/support/docs/wireless-mobility/wireless-lan-wlan/97066-dhcp-option-43-00.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DHCP option 43 for WLC discovery on an IOS DHCP pool

Lightweight APs can use a vendor-specific DHCP option 43 to join a specific wireless LAN controller (WLC) when the
WLC is in a different subnet. RFC 2132 defines the two relevant options: option 60 is the Vendor Class Identifier
(VCI, a text string identifying the device type) and option 43 is the vendor-specific information. Option 60 is
sent in the AP's DHCP discover; matching on it is not required, since your pools can return option 43 to any client.
A server can instead map each VCI to specific controller addresses.

## IOS pool
```
ip dhcp pool <pool-name>
 network <ip-network> <netmask>
 default-router <router-ip>
 dns-server <dns-ip>
 option 43 hex f108c0a80a05c0a80a14
```
The option is defined in each pool (scope) that hands out addresses to the APs. The page's IOS procedure covers
all Cisco IOS Aironet APs except the VxWorks 1000 Series (separate section on the page) and the 600 Series OEAP,
which does not use option 43.

## Building the hex string (classic WLC method)
Type + Length + Value:
- Type is `f1` (0xf1, decimal 241).
- Length is the number of controller management IP addresses times 4, in hex.
- Value is the management IP addresses in hex, one after another.

Worked examples from the page:
- One WLC 192.168.1.10: `f104.c0a8.010a`.
- Two WLCs 192.168.1.10 and 192.168.1.11: `f108.c0a8.010a.c0a8.010b`.
- Two WLCs 192.168.10.5 and 192.168.10.20: `f108c0a80a05c0a80a14` (IOS line `option 43 hex f108c0a80a05c0a80a14`).

Newer variants on the same page use other types: `f2` start converts a group of APs from EWC to CAPWAP mode, and
`f3` is the DHCPv4 fast offline migration form (example `f305ac10011802` replacing `f104ac100118`), understood by
Wave 2, Wi-Fi 6 and Wi-Fi 6E APs on IOS-XE 17.15.2 or later, which ignore the migration part and still read the WLC
address. Check the page for the AP models you run.

## Verify
- [ ] `show ip dhcp binding` on the IOS server lists the lease for the AP.
- [ ] A console-connected older AP logs `Controller address <WLC> obtained through DHCP`.
- [ ] On a classic WLC, `show ap summary` shows the AP registered; `debug dhcp message enable` shows the
  DHCP discover/request sequence and the vendor class id seen by the controller.

## Checked
Date: 2026-11-08. Read the background, option 43/60, classic and migration provisioning, Cisco IOS DHCP server, verify and
troubleshoot sections (the Microsoft, ISC and Lucent QIP server sections only skimmed): Cisco "Configure DHCP
OPTION 43 for Lightweight Access Points" (document 97066). The second cited page (IOS DHCP
server configuration guide) returned 404 and was dropped.
Confirmed: option 43/60 roles, the f1 TLV format and all worked examples, the IOS pool syntax, exclusions for 1000
Series and 600 OEAP, f2/f3 notes, and the verification commands.
Removed: option 150 (phone TFTP), options 66/67 and `next-server`, the `ip`/`ascii`/`hex` option type list, the
Aironet 1000 ASCII comma-list note, pool inheritance and `class`/`match option 60` claims, `show ip dhcp pool` and
`debug ip dhcp server packet detail`, and the capture and `SEP<MAC>.cnf.xml` checks (none on the page).
Method: documentation only; no commands were run.
