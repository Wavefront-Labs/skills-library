---
id: computing-software.systems-network-administration.dns-dhcp.proxydhcp-for-pxe
name: proxydhcp-for-pxe
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [pxe, proxydhcp, dnsmasq, network-boot, port-4011, option-60, wds]
level: practitioner
status: verified
description: "Add PXE boot to a network without touching the main DHCP server using ProxyDHCP: how the PXEClient exchange works, dnsmasq proxy config, port 4011, and relay considerations."
sources:
  - https://thekelleys.org.uk/dnsmasq/docs/dnsmasq-man.html
  - https://www.rfc-editor.org/rfc/rfc4578
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ProxyDHCP for PXE

The existing DHCP server (Windows, router, Kea managed by another team) keeps handing out
addresses. A ProxyDHCP server answers only PXE clients with boot information (next-server, boot
file), not addresses.

## How it works
1. PXE client broadcasts DHCPDISCOVER with option 60 `PXEClient:Arch:xxxxx:UNDI:yyyzzz` (the string iPXE builds in
   `dhcp.h`) and option 93 carrying the client architecture.
2. Normal DHCP server sends an OFFER with an address.
3. ProxyDHCP sends its own OFFER with no address, option 60 `PXEClient`, boot server and file (or
   a PXE menu in option 43).
4. Client takes the address from (2), then talks to the proxy (broadcast port 67 or unicast UDP
   port 4011; iPXE defines `PXE_PORT 4011`) to get boot details, then downloads via TFTP/HTTP.

dnsmasq's man page confirms the mode: "For IPv4, the mode may be proxy in which case dnsmasq will provide proxy-DHCP on the
specified subnet" (see `--pxe-prompt` and `--pxe-service`), and `--port=0` disables the DNS function, leaving DHCP/TFTP.

## dnsmasq as ProxyDHCP
```
port=0                                   # no DNS
dhcp-range=10.0.20.0,proxy               # proxy mode for this subnet
enable-tftp
tftp-root=/srv/tftp
dhcp-match=set:efi64,option:client-arch,7
dhcp-match=set:efi64,option:client-arch,9
pxe-service=tag:!efi64,x86PC,"BIOS boot",pxelinux.0
pxe-service=tag:efi64,x86-64_EFI,"UEFI boot",shimx64.efi
log-dhcp
```
`pxe-service` lines answer the PXE menu; `--dhcp-match=set:tag,option:client-arch,N` tags clients whose option 93 contains N
(man page example uses 6 for EFI IA32). The dnsmasq man page lists the `pxe-service` types as x86PC, PC98, IA64_EFI, Alpha,
Arc_x86, Intel_Lean_Client, IA32_EFI, x86-64_EFI, Xscale_EFI, BC_EFI, ARM32_EFI and ARM64_EFI. Architecture values: the IANA
registry lists 7 as x64 UEFI and 9 as EBC, while RFC 4578's own table calls 9 "EFI x86-64", which is why configs often
match both 7 and 9; match only 7 if you do not need to serve firmware that reports 9.

## Across subnets
The relay (IP helper) must forward client broadcasts to both the main DHCP server and the proxy (two relay targets for the
VLAN; the exact command is device specific and was not run here).
Port 4011 traffic is unicast from client to proxy; routing and firewalls must allow UDP 4011 and TFTP
(UDP 69 plus ephemeral data ports) or HTTP.

## Gotchas
- Do not set options 66/67 on the main DHCP server as well; clients may get conflicting boot info.
- Run one proxy per subnet unless you separate them by tag: two servers offering boot information to the same client can conflict.
- Test each firmware model with a capture before rollout.

## Verify
- [ ] A capture shows both offers, the 4011 exchange, and the TFTP/HTTP download; the client boots
  the right loader for its architecture.
