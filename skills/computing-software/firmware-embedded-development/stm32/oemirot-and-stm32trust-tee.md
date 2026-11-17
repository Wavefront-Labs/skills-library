---
id: computing-software.firmware-embedded-development.stm32.oemirot-and-stm32trust-tee
name: oemirot-and-stm32trust-tee
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-security, oemirot, stirot, stm32trust-tee, tf-m, secure-boot-chain, stm32, firmware-embedded-development]
level: advanced
status: gated
description: "Set up OEMiRoT secure boot (MCUboot based) on STM32U5/H5/L5 with STM32CubeU5/H5 projects: keys, image signing, provisioning scripts and the STiRoT option on H5."
sources:
  - https://wiki.st.com/stm32mcu/wiki/Security:OEMiRoT_OEMuRoT_for_STM32H5
  - https://wiki.st.com/stm32mcu/wiki/Security:Introduction_to_STM32Trust_TEE
  - https://www.st.com/en/embedded-software/x-cube-sbsfu.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OEMiRoT and STM32Trust TEE

For TrustZone parts (L5, U5, H5), ST replaced SBSFU with MCUboot-based roots of trust:
- **OEMiRoT**: OEM immutable Root of Trust, an MCUboot bootloader you build and protect (HDP,
  WRP, RDP). Verifies and optionally decrypts secure and non-secure images, supports swap/overwrite
  updates and anti-rollback.
- **STiRoT** (H5 only, H573): ST immutable RoT in system flash; no bootloader to maintain.
  Can chain to OEMuRoT (updatable RoT) for application update logic.
- **STM32Trust TEE** builds on TF-M for secure services (crypto, storage, attestation).

## Project structure (STM32CubeU5/H5)
`Projects/<board>/Applications/ROT/OEMiRoT_Boot`, `OEMiRoT_Appli_TrustZone`, plus
`ROT_Provisioning/OEMiRoT/` scripts. The `provisioning.bat/.sh` script walks through:
1. Build the bootloader (keys in `Keys/`), secure and non-secure apps.
2. Generate signed images with `imgtool` (from MCUboot via the ROT_AppliConfig tool):
   ```bash
   imgtool sign -k Keys/OEMiRoT_Authentication_S.pem -v 1.0.0 -S 0x20000 \
     -H 0x400 --pad-header --security-counter 1 tfm_s.bin tfm_s_sign.bin
   ```
3. Set option bytes: TZEN=1, SECBOOTADD to the bootloader, watermarks for secure areas, WRP on
   bootloader, HDP area, then RDP.
4. Flash images and the provisioning data via CubeProgrammer scripts.

## Keys
Replace the example keys in `Keys/` before production (`imgtool keygen -t ecdsa-p256`). Example
keys are public: images signed with them prove nothing.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Product state (H5)
H5 uses `PRODUCT_STATE` (Open, Provisioning, Provisioned, TZ-Closed, Closed, Locked) instead of
plain RDP. Moving to Closed with a password-protected regression path (DA, debug authentication)
or Locked (permanent).

## Pitfalls
- Run the provisioning scripts on a fresh board; partially applied option bytes (TZEN set, no
  images) can leave a board needing a TZ regression.
- Toolchain/IDE versions must match the package's tested versions; the scripts call specific
  CubeProgrammer CLI options.

## Verify
- [ ] Tampered image (one byte changed) is rejected by the bootloader.
- [ ] Downgrade to lower security counter rejected.
- [ ] Production keys differ from the package examples.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com, wiki.st.com); no readable alternative was found.

Method: documentation only; no commands were run.
