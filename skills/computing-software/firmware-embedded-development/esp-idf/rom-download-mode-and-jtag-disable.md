---
id: computing-software.firmware-embedded-development.esp-idf.rom-download-mode-and-jtag-disable
name: rom-download-mode-and-jtag-disable
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-security, download-mode, secure-download-mode, jtag-disable, production-lockdown, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Lock down ESP32 production devices by setting secure download mode or disabling ROM download mode and JTAG via eFuses, and know what each choice prevents."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/security/security.rst
  - https://github.com/espressif/esp-idf/blob/master/components/bootloader/Kconfig.projbuild
  - https://github.com/espressif/esp-idf/blob/master/docs/en/security/flash-encryption.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ROM download mode and JTAG disable

The ROM serial bootloader (download mode, entered by the chip's strapping pins) is what esptool talks
to. On a shipped product it is both an attack path and a recovery path.

## Options
| Setting | Effect | Reversible |
|---|---|---|
| Normal download mode | full esptool access | yes |
| Secure UART download mode (`CONFIG_SECURE_UART_ROM_DL_MODE` secure choice, or `esp_efuse_enable_rom_secure_download_mode()`) | no arbitrary code execution; limited commands (SPI config such as baud rate, basic flash write, `get-security-info`); esptool only with `--no-stub` | no |
| Download mode disabled (`CONFIG_SECURE_DISABLE_ROM_DL_MODE`, or `esp_efuse_disable_rom_download_mode()`) | esptool, espefuse and similar tools no longer work; booting with the download strapping prints an error | no |

Secure download mode exists only on chips that support it. For ESP32 the option applies to chip
revision v3.0 and later (`CONFIG_ESP32_REV_MIN` set accordingly). The option appears when Secure Boot v2
or flash encryption is enabled; the default is the secure mode where supported and the release
configuration is in use, otherwise download mode stays enabled so development is not locked out.

## Setting it
Preferred: set `CONFIG_SECURE_UART_ROM_DL_MODE` in the project so the app burns the eFuse on startup
together with the other security features. The runtime functions above do the same from code.

## JTAG
- By default the bootloader permanently disables JTAG on first boot when Secure Boot or flash
  encryption is enabled; `CONFIG_SECURE_BOOT_ALLOW_JTAG` keeps it on for testing environments only
  (it negates flash encryption and part of Secure Boot).
- JTAG can also be disabled without other security features through the eFuse API.
- On chips with the HMAC peripheral JTAG can be soft-disabled and re-enabled by programming a secret
  key through HMAC.

## Consequences
- No serial recovery once download mode is disabled: a bad OTA or bricked app cannot be reflashed over
  UART. Make OTA rollback robust first.
- Do all serial programming, calibration and eFuse writes before the lockdown step; lockdown last.

## Verify
- [ ] `idf.py efuse-summary` on a locked unit shows the intended bits.
- [ ] esptool cannot read the flash of a production unit (secure mode) or cannot connect (disabled).
- [ ] A JTAG probe cannot connect.

## Checked

2026-10-26, against ESP-IDF master docs and headers (espressif/esp-idf, pushed 2026-10-24). Confirmed in security/security.rst and Kconfig.projbuild: Secure UART Download mode behaviour (arbitrary code not executed, limited commands, esptool needs --no-stub), CONFIG_SECURE_UART_ROM_DL_MODE with the secure-mode and permanently-disabled choices, esp_efuse_enable_rom_secure_download_mode and esp_efuse_disable_rom_download_mode, ESP32 v3.0 only for the option, default JTAG disabling and CONFIG_SECURE_BOOT_ALLOW_JTAG, HMAC soft-disable of JTAG. Removed unconfirmed claims: exact eFuse names per chip, the strapping pin list, exact command-by-command restrictions, USB-Serial-JTAG download eFuse names.

Method: documentation only; no commands were run.
