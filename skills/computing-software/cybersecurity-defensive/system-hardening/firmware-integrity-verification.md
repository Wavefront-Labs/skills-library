---
id: computing-software.cybersecurity-defensive.system-hardening.firmware-integrity-verification
name: firmware-integrity-verification
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [firmware-integrity-verification, uefi, nist-sp-800-193, platform-resilience, measured-boot, firmware-security]
level: advanced
status: draft
description: "Verify system firmware integrity: vendor-signed updates, OEM verification tools, measured boot and attestation, firmware dump comparison, and NIST SP 800-193 resiliency features."
sources: ["https://csrc.nist.gov/pubs/sp/800/193/final", "https://csrc.nist.gov/pubs/sp/800/147/final", "https://github.com/fwupd/fwupd", "https://www.dell.com/support/kbdoc/en-us/000126024/dell-trusted-device"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Firmware integrity verification

Firmware implants (LoJax, MosaicRegressor, CosmicStrand, MoonBounce) survive OS reinstalls and disk
replacement. NIST SP 800-193 frames platform firmware resiliency as **protect, detect, recover**.

## Protect: authenticated updates only
- Firmware updates must be signed by the vendor and verified by the platform before flashing (NIST SP 800-147
  / 800-147B). Check that the platform enforces this ("BIOS update signature verification" options) and
  that downgrade protection is enabled.
- Distribute updates from vendor tools (Dell Command Update, HP Image Assistant, Lenovo System Update,
  LVFS/`fwupd` on Linux, Windows Update UEFI capsules) rather than arbitrary downloads; verify hashes.

## Detect
1. **OEM verification features**:
   - Dell Trusted Device / SafeBIOS: off-host BIOS verification compares the BIOS image against a known-good
     copy in Dell's cloud; results to the console/SIEM.
   - HP Sure Start: hardware-enforced self-healing BIOS with a golden copy; logs integrity events.
   - Lenovo ThinkShield self-healing BIOS.
2. **Measured boot and attestation**: TPM PCR0-7 contain firmware and boot configuration measurements;
   remote attestation (Microsoft Defender for Endpoint device health, Intune device health attestation,
   Keylime on Linux) flags unexpected values. Baseline per model and firmware version.
3. **Firmware dump comparison** for investigations: read SPI flash (CHIPSEC `spi dump`, flashrom on Linux),
   extract with UEFITool/`chipsec_util uefi decode`, compare module lists and hashes against the vendor image of
   the same version.
4. **Linux**: `fwupdmgr security` reports Host Security ID (HSI) checks (SPI write protection, Boot Guard,
   Secure Boot, TPM, IOMMU) with a summary level.
5. **Endpoint security**: some EDRs scan UEFI firmware (e.g. Microsoft Defender UEFI scanner, ESET UEFI
   scanner) and alert on known implant modules.

## Recover
Golden image recovery features (HP Sure Start, Dell BIOS recovery), vendor recovery media, or hardware
replacement for compromised boards; plan this in incident response.

## Programme
- Inventory firmware versions per device (WMI `Win32_BIOS`, `fwupdmgr get-devices`, OEM tools).
- Patch firmware on a defined cadence and for critical advisories.
- Hardware procurement requires Boot Guard / Platform Secure Boot, signed updates, and integrity features.

## Verify
Fleet report shows firmware versions current and integrity verification passing (OEM console or attestation),
`fwupdmgr security` HSI level meets the target on Linux hosts, and an incident playbook covers firmware
compromise.
