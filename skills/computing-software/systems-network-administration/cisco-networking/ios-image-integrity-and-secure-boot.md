---
id: computing-software.systems-network-administration.cisco-networking.ios-image-integrity-and-secure-boot
name: ios-image-integrity-and-secure-boot
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, image-verification, secure-boot, trust-anchor, verify-md5, software-authenticity, show-software-authenticity, supply-chain]
level: practitioner
status: draft
description: "Verify IOS XE image integrity and Secure Boot: hash checks against Cisco values, embedded signatures, show software authenticity and Trust Anchor module checks."
sources:
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/sec_usr_cfg/configuration/xe-16/sec-usr-cfg-xe-16-book/sec-image-verification.html
  - https://www.cisco.com/c/en/us/about/trust-center/technical-security-features.html
  - https://sec.cloudapps.cisco.com/security/center/resources/integrity_assurance.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Image integrity and secure boot verification

## Before install: hash and signature
```
verify /sha512 flash:cat9k_iosxe.17.09.05.SPA.bin
verify flash:cat9k_iosxe.17.09.05.SPA.bin        ! checks the embedded Cisco signature
```
Compare the SHA-512 with the value on software.cisco.com for that file. MD5 alone is weak; use SHA-512.
`file verify auto` makes the device verify image signatures on copy (classic IOS).

## Secure Boot (hardware anchored)
Modern Cisco platforms have a hardware Trust Anchor module (TAm) and microloader that verify the
ROMMON and the IOS XE image signatures before execution. A tampered image fails to boot.
```
show software authenticity running               ! signature details of running image packages
show software authenticity keys                  ! keys used to verify (release vs special)
show software authenticity file flash:<IMAGE>.bin
show platform integrity sign nonce 12345         ! signed measurements of boot stages (TAm), IOS XE
show version | include ROM|BOOTLDR
```
`show platform integrity` output lists PCR-style hashes for boot loader, OS and the signature;
compare against Cisco's published known-good values (Cisco "Integrity Assurance" guidance).

## Integrity checks for compromise
Following Cisco integrity guidance after an incident or for high-assurance networks:
- Confirm image hash on flash matches Cisco's published hash.
- `show software authenticity running` shows `Cisco Systems` release keys, not dev keys.
- Compare running memory text segment hash (`verify /md5 system:memory/text` on classic IOS) with Cisco values.
- Check ROMMON version against expected; unexpected ROMMON is a red flag.
- Look for unexpected files on flash and unexpected `boot system` entries.

## Gotchas
- Special/engineering images signed with special keys trigger warnings; only use with TAC.
- Downgrading to old ROMMON may be blocked by anti-rollback on Secure Boot platforms.

## Verify
- [ ] Every deployed image's SHA-512 recorded in your inventory and matches Cisco.
- [ ] `show software authenticity running` clean on all devices (automate with your audit tool).
