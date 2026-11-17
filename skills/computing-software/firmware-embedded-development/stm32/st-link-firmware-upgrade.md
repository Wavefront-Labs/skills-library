---
id: computing-software.firmware-embedded-development.stm32.st-link-firmware-upgrade
name: st-link-firmware-upgrade
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-programmer, st-link-upgrade, stlinkupgrade, st-link-v3, probe-firmware, stm32, firmware-embedded-development]
level: practitioner
status: draft
description: "Upgrade and troubleshoot ST-LINK probe firmware (V2, V2-1, V3, onboard Nucleo/Discovery) with STLinkUpgrade or CubeProgrammer, including VCP/MSD modes and J-Link conversion."
sources:
  - https://www.st.com/en/development-tools/stsw-link007.html
  - https://www.st.com/resource/en/technical_note/tn1235-overview-of-stlink-derivatives-stmicroelectronics.pdf
  - https://www.segger.com/products/debug-probes/j-link/models/other-j-links/st-link-on-board/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ST-LINK firmware upgrade

Outdated ST-LINK firmware causes failures with new STM32 parts or tool versions: "ST-LINK
firmware version not compatible", missing target support, flaky connections.

## Upgrade
- **STLinkUpgrade** (STSW-LINK007, Java, also bundled in CubeIDE/CubeProgrammer):
  1. Close all tools using the probe (CubeIDE debug, CubeProgrammer, CubeMonitor, OpenOCD).
  2. Run `STLinkUpgrade` (or `java -jar STLinkUpgrade.jar`), Refresh device list, Open in update
     mode, Upgrade.
- **CubeProgrammer GUI**: "Firmware upgrade" button in the ST-LINK configuration panel.
- **CubeIDE** prompts when it detects old firmware at debug launch.

## Firmware variants (onboard ST-LINK/V2-1, V3)
The version string shows features: `V2J43M28` = V2, JTAG API 43, Mass storage + VCP (M) version
28. For V2-1 you may choose "STM32 Debug + Mass storage + VCP" or "STM32 Debug + VCP" (drop the
MSD drag-and-drop drive, which some corporate PCs block or which triggers antivirus scans).

## V3 specifics
STLINK-V3SET/MINIE/PWR support bridge functions (SPI/I2C/CAN/GPIO via the Bridge API), higher SWD
clocks (up to 24 MHz), and multiple interfaces. Keep the V3 firmware and CubeProgrammer in sync.

## Converting onboard ST-LINK to J-Link
SEGGER provides a reflash utility turning Nucleo/Discovery onboard ST-LINK into a J-Link OB
(licence restricted to ST evaluation boards). Revert with SEGGER's tool and then STLinkUpgrade.
Useful for RTT and J-Link tooling; not allowed for custom boards.

## Troubleshooting
- Probe not found after upgrade: unplug/replug, reinstall ST-LINK USB driver (STSW-LINK009) on Windows.
- Upgrade fails mid-way: retry in update mode; ST-LINK bootloader stays available.
- Clones (blue "ST-LINK V2" dongles with STM32F103 or clone MCUs): official upgrade may reject or
  brick them. Use genuine probes for production.

## Verify
- [ ] Probe firmware version recorded per test station.
- [ ] CubeProgrammer connects without version warnings.
