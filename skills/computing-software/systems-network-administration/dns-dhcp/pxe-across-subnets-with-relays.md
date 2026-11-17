---
id: computing-software.systems-network-administration.dns-dhcp.pxe-across-subnets-with-relays
name: pxe-across-subnets-with-relays
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [pxe, pxe-relay, ip-helper-address, dhcp-relay, network-boot, proxydhcp]
level: practitioner
status: draft
description: "Make PXE work across routed subnets: ip helper-address to DHCP and PXE servers, next-server/option 66/67 vs proxyDHCP, firewall ports and common pitfalls."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ip/dynamic-address-allocation-resolution/27470-100.html
  - https://learn.microsoft.com/en-us/troubleshoot/mem/configmgr/os-deployment/boot-from-pxe-server
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PXE across subnets

PXE clients broadcast DHCP Discovers with vendor class `PXEClient`. Broadcasts stop at the router,
so relays must forward them to every server that should answer.

## Two designs
1. **DHCP server provides boot info**: options 66 (TFTP server) / `next-server` (siaddr) and 67
   (boot file). Relay needs only the DHCP server as helper.
2. **Separate PXE server (WDS/SCCM/MECM, FOG, proxyDHCP)**: the PXE server answers with boot info only.
   Relay forwards to both:
```
interface Vlan30
 ip helper-address 10.0.0.67      ! DHCP server
 ip helper-address 10.0.0.80      ! PXE/WDS server
```
Prefer design 2 for MECM; Microsoft discourages options 60/66/67 with WDS because they break
UEFI/BIOS selection.

## UEFI and BIOS mix
Options 66/67 give one file for all clients. Use class-based boot files (option 93 arch) on the DHCP
server, or let the PXE server choose (WDS does this automatically).

## Ports and firewalls between client subnets and servers
UDP 67/68 (DHCP), UDP 4011 (PXE/proxyDHCP), UDP 69 + high ports (TFTP), TCP 80/443 for HTTP boot/iPXE.
`ip forward-protocol udp 4011` is not needed with helper-address for normal DHCP ports, but
`ip helper-address` only forwards specific UDP ports by default (67, 69, 53, 37, 49, 137, 138).

## Pitfalls
- DHCP snooping dropping offers from the PXE server on untrusted ports.
- STP without portfast: PXE ROM gives up before the port forwards.
- Relay giaddr in a different subnet than the scope (see Kea relay subnet selection).

## Verify
- [ ] A capture on the client VLAN shows offers from both DHCP and PXE servers (or one with boot options) and the TFTP/HTTP download succeeding.
