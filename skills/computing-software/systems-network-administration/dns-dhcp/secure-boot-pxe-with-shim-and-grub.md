---
id: computing-software.systems-network-administration.dns-dhcp.secure-boot-pxe-with-shim-and-grub
name: secure-boot-pxe-with-shim-and-grub
category: computing-software
field: systems-network-administration
product: dns-dhcp
tags: [pxe, secure-boot-pxe, shim, uefi, grub, network-boot]
level: practitioner
status: draft
description: "PXE boot UEFI machines with Secure Boot enabled using signed shim and GRUB, DHCP architecture options, SBAT revocations and common failure messages."
sources:
  - https://wiki.debian.org/SecureBoot
  - https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/9/html/interactively_installing_rhel_over_the_network/preparing-network-based-repositories
  - https://github.com/rhboot/shim/blob/main/SBAT.md
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Secure Boot with shim and signed GRUB

With Secure Boot on, UEFI firmware only runs binaries signed by keys in its db (normally Microsoft's
UEFI CA). Linux network boot uses **shim** (signed by Microsoft) which then verifies **GRUB** and the
kernel signed by the distribution.

## Files (TFTP or HTTP root)
```
shimx64.efi         # from shim-signed package (Debian: /usr/lib/shim/shimx64.efi.signed)
grubx64.efi         # signed GRUB from the same distro (grubnetx64.efi.signed on Debian/Ubuntu)
grub/grub.cfg       # or grub.cfg-01-<mac> per host
vmlinuz, initrd     # signed distribution kernel
```
shim loads `grubx64.efi` from the same directory by name; keep names exact.

## DHCP
Serve shim to UEFI x64 clients (option 93 = 0x0007 or 0x0009); BIOS clients (0x0000) get pxelinux:
```json
{ "name": "uefi-x64", "test": "option[93].hex == 0x0007 or option[93].hex == 0x0009", "boot-file-name": "shimx64.efi" }
```
UEFI HTTP Boot clients (0x0010) can use a URL boot file.

## Failures
| Message | Cause |
|---------|-------|
| `Verification failed: (0x1A) Security Violation` | unsigned or wrongly signed GRUB/kernel, mixed distros |
| `SBAT self-check failed` / revoked | old shim/GRUB revoked by SBAT or dbx updates (2022+ BootHole/2024 updates); update shim and GRUB |
| Firmware ignores PXE file | Secure Boot rejects unsigned shim builds; use distro signed packages |
| GRUB prompt, no menu | grub.cfg path wrong (`prefix`), check TFTP logs for requested paths |

## Custom kernels
Sign with your own key and enrol it in MOK (`mokutil --import`), which needs console interaction once
per machine; or keep Secure Boot-compatible distro kernels for installers.

## Verify
- [ ] A Secure Boot-enabled test machine loads shim, GRUB menu and the installer kernel; `mokutil --sb-state` in the installed system reports SecureBoot enabled.
