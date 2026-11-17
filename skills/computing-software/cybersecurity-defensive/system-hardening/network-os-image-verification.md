---
id: computing-software.cybersecurity-defensive.system-hardening.network-os-image-verification
name: network-os-image-verification
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [image-verification, network-device-hardening, firmware-integrity, cisco-secure-boot, hash-verification, supply-chain]
level: practitioner
status: draft
description: "Verify network OS images before and after install: vendor hashes and signatures, on-device verify commands, secure boot and runtime integrity checks for routers and switches."
sources: ["https://www.cisco.com/c/en/us/about/trust-center/technology-built-in-security.html", "https://sec.cloudapps.cisco.com/security/center/resources/integrity_assurance.html", "https://www.cisa.gov/resources-tools/resources/network-infrastructure-security-guide", "https://www.juniper.net/documentation/us/en/software/junos/software-installation-and-upgrade/topics/topic-map/software-validation.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Network OS image verification

Attackers who own a router can install modified firmware or in-memory implants (e.g. SYNful Knock on Cisco
IOS, 2015; more recent edge-device campaigns). Verify images at every stage.

## Before upload
1. Download only from the vendor portal over HTTPS.
2. Compare the published hash (SHA-512 on Cisco Software Download, SHA-256 on Juniper downloads):
   `sha512sum image.bin` and compare character by character (or with a script).
3. Where the vendor signs images, verify the signature (Junos packages are signed and validated at install;
   Cisco IOS XE images are digitally signed and verified by the boot process).
4. Store approved images in an internal, access-controlled repository with recorded hashes.

## On the device
- Cisco IOS/IOS XE: `verify /md5 flash:image.bin <expected-md5>` or `verify /sha512 flash:image.bin`;
  `show software authenticity running` and `show software authenticity file flash:image.bin` show signature
  verification (on platforms with image signing).
- Cisco NX-OS: `show file bootflash:image.bin sha512sum`.
- Junos: `request system software validate` before install; `show system software` after; Junos verifies
  package signatures automatically (Veriexec on FreeBSD-based Junos blocks unsigned executables).
- Arista EOS: `verify /sha512 flash:EOS.swi`.
- After boot: confirm the running version and image path match what you installed (`show version`).

## Secure boot and runtime integrity
- Hardware anchored secure boot (Cisco Trust Anchor module, Juniper secure boot on newer platforms) verifies
  the bootloader and OS signatures; ensure it is enabled and not in a debug/override mode.
- Cisco IOS integrity assurance guidance: compare `show version`, `show region`/memory text checksums
  (`verify /md5 system:memory/text` on supported IOS) against known-good values from the same image to detect
  in-memory modification.
- Remote attestation via TPM where the platform supports it (e.g. some IOS XR and Junos Evolved platforms).

## Process controls
- Change tickets record expected hash; post-change check records actual hash.
- Periodic integrity audits (quarterly or after suspected compromise) on the running image and boot variables
  (`show boot`, `show bootvar`) to catch unexpected images.
- Restrict who can copy files to flash (AAA command authorization for `copy`, `boot system`).

## Verify
Last upgrade ticket shows matching vendor hash and on-device verify output; `show software authenticity running`
reports a valid signature; boot variables point to the approved image.
