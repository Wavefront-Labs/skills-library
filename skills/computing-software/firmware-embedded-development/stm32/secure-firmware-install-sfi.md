---
id: computing-software.firmware-embedded-development.stm32.secure-firmware-install-sfi
name: secure-firmware-install-sfi
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-programmer, sfi, secure-firmware-install, trusted-package-creator, stm32-hsm, stm32, firmware-embedded-development]
level: advanced
status: gated
description: "Program encrypted firmware into STM32 parts at untrusted manufacturers with Secure Firmware Install (SFI): Trusted Package Creator, STM32HSM licences and CubeProgrammer flow."
sources:
  - https://www.st.com/resource/en/application_note/an4992-overview-secure-firmware-install-sfi-stmicroelectronics.pdf
  - https://www.st.com/resource/en/user_manual/um2238-stm32-trusted-package-creator-tool-software-description-stmicroelectronics.pdf
  - https://www.st.com/en/development-tools/stm32hsm-v2.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Secure firmware install (SFI)

SFI protects firmware confidentiality and limits the number of units a contract manufacturer
can program. The firmware is encrypted on the OEM side; only genuine STM32 devices with an
SFI-capable bootloader (root security services in system memory) can decrypt it, and an HSM
smart card meters the number of installs.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Supported parts
STM32H7 (H72x/H73x, H7A/B, H74x/H75x rev V), L4/L4+ selected lines, L5, U5, WB, WL, H5 (SFI
via STiRoT/OEMiRoT flows). Check AN4992 and your part's AN for the exact flavour (SFI, SSFI,
SMI for modules).

## Steps
1. **Package (OEM)**: STM32 Trusted Package Creator encrypts the image (AES-GCM) into an `.sfi`
   file, with the option bytes and areas to program:
   ```bash
   STM32TrustedPackageCreator_CLI -sfi -fir app.hex -k key.bin -n nonce.bin -v 1 -ob ob.csv -o app.sfi
   ```
2. **Provision HSM (OEM)**: program an STM32HSM card with the same key and a counter (max number of
   devices), using Trusted Package Creator's HSM programming.
3. **Install (factory)**: CubeProgrammer talks to the device bootloader (UART, USB, SPI, or
   JTAG/SWD depending on part) and the HSM:
   ```bash
   STM32_Programmer_CLI -c port=SWD mode=HOTPLUG -sfi protocol=static "app.sfi" hsm=1 slot=1
   ```
   The device generates a session key with the HSM; the HSM decrements its counter per install.
4. The device ends with RDP level set as packaged (typically level 1 or 2), so the decrypted
   image can't be read back.

## Considerations
- Keep AES keys and the `.sfi` creation in the OEM secure environment; the factory only gets the
  encrypted file and the HSM.
- Test the full SFI on engineering samples: some option byte combinations are refused.
- SFI doesn't replace secure boot: pair with SBSFU/OEMiRoT for authenticated updates in the field.

## Verify
- [ ] Device programmed via SFI boots and its RDP level matches the package.
- [ ] HSM counter decrements per unit; exhausted HSM blocks further installs.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.
