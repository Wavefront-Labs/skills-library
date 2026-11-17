---
id: computing-software.systems-network-administration.dns-dhcp.pxe-error-codes
name: pxe-error-codes
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [pxe, pxe-errors, network-boot, tftp, uefi-pxe, secure-boot, troubleshooting]
level: practitioner
status: draft
description: "Decode PXE boot failures: PXE-E51/E53/E32/E11 and UEFI equivalents, where each fails (DHCP, boot file, TFTP), and the matching fixes on DHCP, relay, TFTP and Secure Boot."
sources:
  - https://www.rfc-editor.org/rfc/rfc4578
  - https://learn.microsoft.com/en-us/troubleshoot/mem/configmgr/os-deployment/troubleshoot-pxe-boot-issues
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PXE error codes

## Legacy BIOS PXE (Intel PXE ROM messages)
| Message | Stage | Typical cause |
|---|---|---|
| PXE-E51: No DHCP or proxyDHCP offers were received | DHCP | no relay/helper for the VLAN, STP delay (no PortFast), 802.1X port unauthorised, DHCP pool full |
| PXE-E53: No boot filename received | DHCP options | option 67 / boot file missing, or ProxyDHCP not answering |
| PXE-E32: TFTP open timeout | TFTP | next-server (siaddr/option 66) wrong or unreachable, firewall blocks UDP 69 or the ephemeral data ports |
| PXE-E3B: TFTP error - File Not Found | TFTP | path/case of the boot file wrong (Linux TFTP is case-sensitive) |
| PXE-E11: ARP timeout | ARP | TFTP server or gateway not answering ARP, wrong subnet |
| PXE-E55: ProxyDHCP service did not reply to request on port 4011 | ProxyDHCP | port 4011 blocked or proxy not running |
| PXE-E61: Media test failure, check cable | link | no link, wrong NIC enabled for PXE |

## UEFI messages
- `Start PXE over IPv4` then return to boot menu: no offer (same causes as E51) or no boot file.
- `PXE-E16: No valid offer received` (some firmware): offer lacked boot info for this arch (option 93
  matching wrong; serving a BIOS file to a UEFI client).
- `Access Denied` / `Image failed to verify with Secure Boot`: unsigned loader with Secure Boot on;
  use signed shim + GRUB or WDS's signed bootmgfw.efi.
- `TFTP Error: Buffer too small`: blksize negotiation problem; adjust tftpd max blksize.

## Workflow
1. Capture on the PXE server or a SPAN of the client port: did DISCOVER arrive? Which offers went
   back? (`udp port 67 or udp port 68 or udp port 4011 or udp port 69`)
2. Check option 93 (client arch) in the DISCOVER and that the offer's boot file matches it.
3. Test TFTP from the client subnet: `tftp -m binary 10.0.0.30 -c get bootx64.efi`.

## Gotchas
- Spanning tree: PXE ROMs give up before a legacy STP port reaches forwarding (30 s); PortFast on
  edge ports.
- Many UEFI clients prefer IPv6 PXE first if enabled; disable PXE over IPv6 in firmware or serve it.

## Verify
- [ ] The client progresses past DHCP and TFTP into the loader; capture shows a clean
  DORA + TFTP sequence.
