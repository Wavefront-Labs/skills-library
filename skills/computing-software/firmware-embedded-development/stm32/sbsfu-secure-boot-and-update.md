---
id: computing-software.firmware-embedded-development.stm32.sbsfu-secure-boot-and-update
name: sbsfu-secure-boot-and-update
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-security, sbsfu, x-cube-sbsfu, secure-engine, prepareimage, secure-firmware-update, stirot-oemirot, stm32, firmware-embedded-development]
level: sme
status: draft
description: "Use ST's X-CUBE-SBSFU (Secure Boot and Secure Firmware Update) on STM32: architecture, crypto scheme choice, key provisioning, packaging .sfb images, and when to use STiROT/OEMiROT instead."
sources:
  - https://www.st.com/en/embedded-software/x-cube-sbsfu.html
  - https://www.st.com/resource/en/user_manual/um2262-getting-started-with-the-xcubesbsfu-stm32cube-expansion-package-stmicroelectronics.pdf
  - https://www.st.com/resource/en/application_note/an5056-integration-guide-for-the-xcubesbsfu-stm32cube-expansion-package-stmicroelectronics.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SBSFU secure boot and update

X-CUBE-SBSFU is ST's reference secure bootloader for STM32 series **without** TrustZone (F4,
F7, G0, G4, H7, L0, L1, L4, WB, WL). It verifies the application at every boot and installs
encrypted, signed updates. For TrustZone parts (L5, U5, H5) ST provides TF-M based SBSFU and the
STiROT/OEMiROT (MCUboot-derived) root-of-trust instead; use those for new designs on them.

## Architecture
- **SBSFU** (immutable after production): runs first, checks the active slot, installs updates.
- **Secure Engine (SE)**: isolated code and keys (protected by the Firewall on L0/L4, or
  MPU-based isolation elsewhere), exposes crypto services through a call gate.
- **User app**: in slot 0 (active); updates downloaded into slot 1 (dual-slot) or swapped
  (single-slot with swap area, depending on the example).
- Protections applied by SBSFU at boot: RDP, WRP on SBSFU/SE, PCROP on keys, MPU, IWDG, DAP
  disabled. During development `SECBOOT_DISABLE_SECURITY_IPS` turns these off.

## Crypto scheme (choose in `SECBOOT_CRYPTO_SCHEME`)
| Scheme | Authenticity | Confidentiality |
|---|---|---|
| `SECBOOT_ECCDSA_WITH_AES128_CBC_SHA256` | ECDSA P-256 signature (asymmetric) | AES-128-CBC |
| `SECBOOT_ECCDSA_WITHOUT_ENCRYPT_SHA256` | ECDSA P-256 | none |
| `SECBOOT_AES128_GCM_AES128_GCM_AES128_GCM` | AES-GCM tag (symmetric) | AES-GCM |
Asymmetric signing is preferred: the device holds only the public key for verification, so
extracting it from one device doesn't let an attacker sign firmware. The AES key for
decryption is still a shared secret; protect it with PCROP/firewall.

## Keys and build
Keys live in the SE project (`Binary/` folder: `ECCKEY1.txt`, `OEM_KEY_COMPANY1_key_AES_CBC.bin`).
The SE build embeds them; replace the example keys before anything leaves the lab. The
`prepareimage.py` post-build step (in `Middlewares/ST/STM32_Secure_Engine/Utilities/KeysAndImages`)
produces:
- `.sfb` update file (header + encrypted firmware + signature),
- `.bin` combining SBSFU and app for factory programming.
Header carries version: SBSFU refuses older versions (anti-rollback).

## Updating
Local loader: YModem over UART in SBSFU (development and recovery). In the field the app
downloads the `.sfb` into the download slot and requests installation (reboot). Installation is
resumable after power loss (the swap/copy is journaled).

## Practical advice
- Start from the exact example for your board, then port: memory map (linker files in
  `Linker_Common`), clocks, UART. Most bring-up pain is memory layout.
- Keep SBSFU size small; it can't be updated in the field.
- Measure boot time: hash and signature verification of a large image adds hundreds of ms.
- Production: program SBSFU+SE+app combined image, then let SBSFU set protections on first boot
  (or set RDP in the line); verify with a debugger that DAP is closed.

## Verify
- [ ] Tampered `.sfb` (one byte flipped) is rejected; device keeps running old firmware.
- [ ] Power loss during installation (relay test) never bricks the device.
- [ ] Release build has security IPs enabled and example keys replaced.
