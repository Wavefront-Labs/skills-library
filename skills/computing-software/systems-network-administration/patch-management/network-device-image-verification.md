---
id: computing-software.systems-network-administration.patch-management.network-device-image-verification
name: network-device-image-verification
category: computing-software
field: systems-network-administration
product: patch-management
tags: [image-verification, patch-integrity, signature-verification, network-device-upgrade, cisco, juniper]
level: practitioner
status: draft
description: "Verify network OS images before booting: vendor SHA-512 hashes, on-device verify commands for Cisco, Juniper, Arista and Fortinet, signed images, and evidence."
sources:
  - https://www.cisco.com/c/en/us/support/docs/ios-nx-os-software/ios-software-releases-121-mainline/200253-Verify-the-Integrity-of-a-Cisco-IOS-Image.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network device image verification

A corrupted transfer bricks a device at reboot; a tampered image is a supply-chain
compromise. Verify **twice**: on the repository server after download, and on the device
after copy.

## Get the reference hash
From the vendor download portal (logged in), not from a mirror or email. Prefer SHA-512
(Cisco shows MD5 and SHA512).

## On the device
| Vendor | Command |
|---|---|
| Cisco IOS/IOS-XE | `verify /sha512 flash:cat9k_iosxe.17.09.05.SPA.bin` (or `/md5`) |
| Cisco NX-OS | `show file bootflash:nxos64-cs.10.3.5.M.bin sha512sum` |
| Cisco ASA/FTD | `verify /sha-512 disk0:/asa9-20-3-smp-k8.bin` |
| Juniper Junos | `file checksum sha256 /var/tmp/junos-....tgz` |
| Arista EOS | `verify /sha512 flash:EOS-4.32.2F.swi` |
| FortiGate | upload via GUI shows checksum validation; CLI `diagnose sys checksum`-style options vary; compare with the `.out` checksum file from support portal |
| Palo Alto | images downloaded via the device are signature-checked; manual uploads also validated at install |

## Signed images
Modern platforms verify vendor signatures at boot/install (Cisco "Digitally Signed Cisco
Software" with `show software authenticity running`, `show software authenticity file
flash:<image>`; Junos validates package signatures automatically). A hash check still
catches truncation before you schedule a reboot.

## Process
1. Download once into an internal repository; record SHA-512 next to the file.
2. Copy to devices (SCP/HTTP), run verify, compare automatically:
   ```python
   # Netmiko/NAPALM style
   out = conn.send_command(f"verify /sha512 flash:{img}", read_timeout=300)
   assert expected_sha512.lower() in out.lower()
   ```
3. Save the output in the change ticket as evidence.
4. Only then set boot variables / install.

## Gotchas
- `verify` on large images can take minutes and CPU; don't time out the script early.
- Free space: verify after copy completes; partial files hash wrong (good, that's the point).
- Different image variants (e.g. NPE vs crypto, universal vs lite) have different hashes:
  match the exact filename.

## Verify
Every upgrade ticket contains matching vendor and device hashes for the installed image.
