---
id: computing-software.firmware-embedded-development.bootloader-development.mcumgr-image-upload
name: mcumgr-image-upload
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [mcumgr, smp-protocol, image-management, firmware-upload, test-and-confirm, smp-ble, smpmgr, zephyr, mcuboot, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Update a running Zephyr/MCUboot device with MCUmgr over UART, BLE or UDP: app-side Kconfig, upload, image test, reset and confirm, plus host tools."
sources:
  - https://docs.zephyrproject.org/latest/services/device_mgmt/mcumgr.html
  - https://docs.zephyrproject.org/latest/services/device_mgmt/smp_groups/smp_group_1.html
  - https://docs.zephyrproject.org/latest/samples/subsys/mgmt/mcumgr/smp_svr/README.html
  - https://github.com/apache/mynewt-mcumgr-cli
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MCUmgr image upload

**Goal:** the application receives a new signed image into the secondary slot while running,
and the update is tested then confirmed through MCUboot's swap and rollback.

## App-side Kconfig (Zephyr)
```
CONFIG_MCUMGR=y
CONFIG_MCUMGR_GRP_IMG=y
CONFIG_MCUMGR_TRANSPORT_UART=y      # or CONFIG_MCUMGR_TRANSPORT_BT / CONFIG_MCUMGR_TRANSPORT_UDP
```
`samples/subsys/mgmt/mcumgr/smp_svr` is the reference: copy its `prj.conf` for the full set of
dependent options rather than hand-picking them. Zephyr's MCUmgr page lists the transports
(UART, raw UART, shell, Bluetooth, UDP over IPv4/IPv6, LoRaWAN, SPI) with their Kconfig symbols.

## Update flow
The Go `mcumgr` CLI (mynewt-mcumgr-cli) example from its README, over BLE:
```sh
CONN="--conntype ble --connstring peer_name=Zephyr"
mcumgr $CONN image list
mcumgr $CONN image upload <signed-image.bin>
mcumgr $CONN image list                     # the new image appears with its hash
mcumgr $CONN image test <image-hash>        # run it on next boot, on trial
mcumgr $CONN reset
mcumgr $CONN image list                     # confirm the new image is running
mcumgr $CONN image confirm
```
- **Test vs confirm** (SMP image group): with `confirm` false or absent, the image with the given
  `hash` is set for test, meaning it is not permanent and, after a hard reset, the previous
  application is restored to the primary slot. With `confirm` true the `hash` is optional and the
  currently running application is confirmed.
- The application can also confirm itself after a health check (network up, sensors OK); look
  up the current MCUboot confirm API in the Zephyr docs. Confirming at the very start of `main()`
  defeats the purpose of rollback.
- `imgtool dumpinfo <signed image>` prints the image hash without uploading it.

## Host tools
- `mcumgr` (Go CLI, apache/mynewt-mcumgr-cli) and `smpmgr` (Python; serial, BLE or UDP). Others
  exist (mobile apps, GUI tools); check each tool's own docs for options.

## Security
SMP has no authentication of its own: anyone who can reach the transport can send commands.
Images must still be signed to boot, but restrict the transport (BLE pairing and encryption,
a management network for UDP) or add authorisation hooks. Zephyr's UDP transport has optional
DTLS support.

## Verify
- [ ] After `test` + reset without confirm + reset again, `image list` shows the old image active.
- [ ] Interrupted upload can be restarted and the final image hash matches.

## Checked
2026-10-31. Confirmed against the Zephyr MCUmgr page (transport table and symbols), SMP image group page
(`confirm`/`hash`/`permanent` semantics, test behaviour), the smp_svr sample README (`imgtool dumpinfo`) and the
mcumgr-cli README (`--conntype`, `--connstring`, `image list/upload/test/confirm`, `reset`). Removed: the extra
Kconfig lines (NET_BUF, ZCBOR, FLASH_MAP, STREAM_FLASH, IMG_MANAGER, GRP_OS, BASE64), the BLE SMP service UUID,
the C confirm snippet, the throughput tuning options and 10-60 KB/s figure, `IMG_ERASE_PROGRESSIVELY`, the
serial connection string and tool descriptions (not found in fetched pages).
Method: documentation only; no commands were run.
