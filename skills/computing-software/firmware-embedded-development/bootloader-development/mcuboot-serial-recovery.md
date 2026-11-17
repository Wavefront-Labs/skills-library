---
id: computing-software.firmware-embedded-development.bootloader-development.mcuboot-serial-recovery
name: mcuboot-serial-recovery
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [mcuboot-serial-recovery, mcuboot, serial-recovery, smp-protocol, mcumgr, cdc-acm, recovery-button, unbrick, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Enable MCUboot serial recovery: UART or USB CDC transport, entry by button, timeout or missing app, uploading with mcumgr, and primary-slot trade-offs."
sources:
  - https://docs.mcuboot.com/serial_recovery.html
  - https://raw.githubusercontent.com/mcu-tools/mcuboot/main/boot/zephyr/Kconfig.serial_recovery
  - https://docs.zephyrproject.org/latest/services/device_mgmt/mcumgr.html
  - https://github.com/intercreate/smpmgr
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MCUboot serial recovery

**Goal:** a device with a broken or missing application can be reflashed over its UART or USB
port without a debug probe, using the bootloader itself.

## How it works
MCUboot implements an SMP (Simple Management Protocol) server with a subset of MCUmgr commands:
OS group `reset` (and `echo` when `BOOT_MGMT_ECHO` is on), IMG group `image list` and
`image upload`. Uploads target the **primary slot by default**, so a recovery upload does not go
through the swap/rollback path: it is a recovery path, not the normal update path.

## Zephyr configuration (MCUboot image, e.g. sysbuild/mcuboot.conf)
```
CONFIG_MCUBOOT_SERIAL=y
CONFIG_BOOT_SERIAL_UART=y          # or CONFIG_BOOT_SERIAL_CDC_ACM=y for USB
CONFIG_BOOT_SERIAL_WAIT_FOR_DFU=y  # optional: wait for an MCUmgr command on every boot
CONFIG_BOOT_SERIAL_WAIT_FOR_DFU_TIMEOUT=500   # ms, default 500
CONFIG_BOOT_SERIAL_NO_APPLICATION=y   # enter recovery if no bootable application
```
Entry triggers (Kconfig "Entrance methods", combine as needed):
- **GPIO** (`CONFIG_BOOT_SERIAL_ENTRANCE_GPIO`, default y when GPIO is enabled);
  `CONFIG_BOOT_SERIAL_DETECT_DELAY` helps when the same button powers the board on.
- **Wait for DFU** (`BOOT_SERIAL_WAIT_FOR_DFU`): MCUboot waits for an MCUmgr command for the
  timeout on every boot, which adds boot latency.
- **Retention boot mode** (`CONFIG_BOOT_SERIAL_BOOT_MODE`, needs Zephyr's boot-mode retention):
  the application sets the boot mode and reboots to request recovery.
- **No valid application** (`BOOT_SERIAL_NO_APPLICATION`).
- **Reset by pin** (`BOOT_SERIAL_PIN_RESET`): stays in recovery if the reset pin caused the reset.

The UART is the devicetree chosen node `zephyr,uart-mcumgr`; if it does not exist, `zephyr,console`
is used, and if both point to the same device the build fails with a compile error. With
`BOOT_SERIAL_CDC_ACM` the CDC ACM port is used unless `zephyr,uart-mcumgr` is chosen, in which
case recovery moves to that UART and the console stays on CDC ACM. The CDC ACM VID/PID default to
Zephyr's values; use your own outside Zephyr samples.
`CONFIG_BOOT_SERIAL_RAW_PROTOCOL` drops the base64/CRC console framing for less flash and RAM and
faster transfers; the host client must then use a matching raw transport.

## Uploading
MCUboot's documentation uses the Go `mcumgr` CLI with a serial connection profile:
```sh
mcumgr conn add serial_1 type="serial" connstring="dev=/dev/ttyACM0,baud=115200"
mcumgr image upload <path-to-signed-image-bin-file> -c serial_1
mcumgr image list -c serial_1
mcumgr reset -c serial_1
```
`smpmgr` (Python) also talks SMP over serial, BLE or UDP. Images must be signed with the key
MCUboot trusts. `CONFIG_MCUBOOT_SERIAL_DIRECT_IMAGE_UPLOAD=y` makes recovery honour the image
number in the upload header (1 = primary slot of the first image, 2 = its secondary slot, and so
on; 0 is the default, same as 1).

## Trade-offs and gotchas
- A failed or interrupted upload to the primary slot leaves no bootable app. Acceptable for
  recovery since you can retry, but not as the field update method.
- The bootloader grows (serial, SMP, CBOR); resize the boot partition and rebuild both images.
- Security: anyone with physical access to the port can upload images signed with a trusted key,
  including old signed versions; enable downgrade prevention in MCUboot or disable serial
  recovery in production builds.
- `CONFIG_BOOT_SERIAL_INACTIVITY_TIMEOUT` (default 0 = never) resets the SoC after a period with
  no MCUmgr command, so an aborted upload does not leave the device stuck in recovery.
- The host tool's baud rate must match the bootloader's UART.

## Verify
- [ ] Erase the app slot: device enters recovery automatically and accepts an upload.
- [ ] Holding the button at reset enters recovery even with a valid app.

## Checked
2026-10-31. Confirmed against the MCUboot serial recovery page, MCUboot `boot/zephyr/Kconfig.serial_recovery`
(option names, defaults, entrance methods, chosen nodes, direct image upload mapping), the Zephyr MCUmgr page
and the smpmgr README (transports). Removed: `CONFIG_UART_CONSOLE=n`, the `mcuboot-button0` alias, size
figures, the MTU remark, the `smpmgr` command line, the claim that older releases used the console UART and the
downgrade-prevention option name (not found in the fetched pages).
Method: documentation only; no commands were run.
