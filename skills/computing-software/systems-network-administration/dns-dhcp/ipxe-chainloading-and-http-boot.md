---
id: computing-software.systems-network-administration.dns-dhcp.ipxe-chainloading-and-http-boot
name: ipxe-chainloading-and-http-boot
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [dhcp, pxe, network-boot, ipxe, chainloading, http-boot, uefi-http-boot, option-77, user-class, option-60-httpclient, snponly-efi, undionly-kpxe, boot-loop, secure-boot]
level: advanced
status: docs-checked
description: "Chainload iPXE from existing PXE firmware over TFTP, avoid the infinite boot loop, and pick BIOS or UEFI binaries by client architecture."
sources:
  - https://ipxe.org/howto/chainloading
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# iPXE chainloading

## Why chainload
Machines that already have a PXE implementation (for example an Intel PXE ROM) can run iPXE without reflashing each network card. Put a copy of iPXE on your TFTP server; each machine downloads it from there at every boot.

## Set up
1. For BIOS machines, download `undionly.kpxe` from boot.ipxe.org into the TFTP directory. For UEFI network boot, download `ipxe.efi` the same way.
2. Make the DHCP server hand out the file as the boot file with `next-server` set to the TFTP server. ISC dhcpd: `next-server X.X.X.X; filename "undionly.kpxe";`.
3. Boot a PXE-capable machine and look for the iPXE start-up banner.

## Choose BIOS or UEFI binary
The iPXE page's ISC dhcpd example uses the client architecture option (option 93) to hand out `ipxe.efi` to anything other than architecture `00:00` and `undionly.kpxe` to BIOS clients. UEFI network booting tends to be much slower than BIOS, and the page suggests BIOS compatibility mode for network boot where the firmware offers it.

## Break the infinite loop
The chainloaded iPXE issues a fresh DHCP request and boots whatever the server hands out. If that is still the iPXE image, the machine loops: PXE loads iPXE, which loads iPXE, and so on. Three fixes from the page:
- **autoexec script:** place a script named `autoexec.ipxe` on the TFTP server beside the iPXE binary (or in the TFTP root); iPXE downloads and runs it automatically. An empty file suppresses the missing-script error and iPXE then boots normally. Not all platforms support it.
- **DHCP server:** hand out iPXE only for the first DHCP request; the second request returns the real boot filename. The page links to ISC dhcpd and Microsoft DHCP server recipes.
- **embedded script:** build iPXE with a script that chains to a fixed URL, for example `make bin/undionly.kpxe EMBED=demo.ipxe` where the script contains `chain http://...`; the chainloaded iPXE then always boots from that URL regardless of DHCP.

## Verify
- [ ] BIOS and UEFI test machines each load the right binary, then the next-stage file, with no loop.

## Checked

Confirmed against the iPXE chainloading how-to (read in full). Removed as not on that page: the Kea client-class JSON, option 77 `iPXE` user-class test, `snponly.efi`, option 60 `HTTPClient` and client architecture 16 for UEFI HTTP boot, the `boot.ipxe` menu example, the Secure Boot paragraph, and the Kea and UEFI specification sources (not read).

Method: docs-checked 2026-11-09 against https://ipxe.org/howto/chainloading.
