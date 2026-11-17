---
id: computing-software.systems-network-administration.network-design.duplicate-mac-addresses
name: duplicate-mac-addresses
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, troubleshooting-services, duplicate-mac, mac-flapping, vm-cloning, mac-address-table]
level: practitioner
status: gated
description: "Find and fix duplicate MAC addresses: symptoms like MAC flapping and intermittent connectivity, cloned VMs and images, virtual MAC conflicts, and locating both devices."
sources:
  - https://www.cisco.com/c/en/us/support/docs/switches/catalyst-6500-series-switches/116130-maintain-mac-address-flapping-00.html
  - https://knowledge.broadcom.com/external/article?legacyId=1024025
  - https://www.rfc-editor.org/rfc/rfc5798
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Duplicate MAC addresses

## Causes
- Cloned VMs with static MAC (copied .vmx, OVA imports set to keep MAC, KVM XML copied).
- Imaged devices with software-defined MACs (some IoT, embedded, cheap USB NICs with identical MACs).
- Two VRRP groups with the same VRID on the same VLAN (the VRRP IPv4 virtual MAC is `00-00-5E-00-01-{VRID}`, so the VRID sets the MAC; HSRP also derives its virtual MAC from the group number).
- Two clusters/firewall HA pairs using the same cluster ID / virtual MAC.
- Spoofing attacks.

## Symptoms
- Intermittent connectivity for two hosts, alternating.
- Switch logs a MAC-flapping message naming the MAC, the VLAN and the two ports (wording varies by platform) (also caused by L2 loops; check STP if many MACs flap).
- ARP entries for two IPs showing the same MAC.

## Locate (IOS-style commands; exact syntax varies by platform) (gated: unconfirmed, source is paywalled or blocked)
```
show mac address-table address 0050.56aa.bb01
show logging | include MACFLAP
show ip arp | include 0050.56aa.bb01
```
On hypervisors, search inventory for the MAC (two vCenter Servers with the same instance ID can generate identical MACs). Linux hosts: `ip link`.

## Fix
- Regenerate MACs on cloned VMs (remove static MAC, let the hypervisor assign), sysprep/generalise
  images.
- Unique VRRP/HSRP group numbers per VLAN; unique HA cluster IDs per segment.
- Port security / DAI to detect spoofing.

## Verify
- [ ] MAC flap logs stop; each MAC appears on one port; both affected hosts stable for 24 h.

## Checked

- Date: 2026-10-28
- Confirmed: RFC 5798: VRRP IPv4 virtual MAC format 00-00-5E-00-01-{VRID}. Broadcom KB: vCenter Servers sharing an instance ID can generate duplicate VM MAC addresses, causing packet loss.
- Removed: the exact Cisco log string and the HSRP virtual MAC pattern (the Cisco MAC-flap page returned 404), the PowerShell inventory command.
- Gated: the IOS-style show commands in the Locate section could not be checked against a Cisco reference page.
Method: documentation only; no commands were run.
