---
id: computing-software.firmware-embedded-development.bootloader-development.ble-dfu-over-the-air
name: ble-dfu-over-the-air
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [firmware-transport, ble-dfu, smp-over-ble, nordic-secure-dfu, att-mtu, data-length-extension, connection-interval, nrf-connect-device-manager, firmware-embedded-development]
level: advanced
status: draft
description: "Update firmware over Bluetooth LE: SMP/MCUmgr vs Nordic Secure DFU, MTU and connection-parameter tuning for throughput, and resuming interrupted transfers."
sources:
  - https://docs.zephyrproject.org/latest/services/device_mgmt/smp_transport.html
  - https://docs.nordicsemi.com/bundle/sdk_nrf5_v17.1.0/page/lib_bootloader_dfu_process.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# BLE DFU (over-the-air via Bluetooth LE)

**Goal:** reliable phone-to-device firmware updates over BLE in a reasonable time (a 300 KB
image in under a minute), robust to disconnects.

## Protocol choices
| Option | Notes |
|---|---|
| **MCUmgr SMP over BLE** (Zephyr/NCS, MCUboot) | image uploaded into the secondary slot while the app runs; MCUboot swaps on reboot. Phone libs: nRF Connect Device Manager (iOS/Android), `mcumgr`/`smpmgr` CLI |
| **Nordic Secure DFU** (nRF5 SDK) | separate DFU bootloader with its own BLE stack; signed init packet + firmware; nRF Connect / nRF DFU library |
| Vendor-specific (ST, Silabs OTA, Espressif BLE OTA component) | similar ideas, own GATT services |
| Custom GATT service | only if none fits; you then own resume, integrity and security |

## Throughput tuning
Effective rate depends on how many bytes go out per connection event:
- **ATT MTU** up to 247-498 (`CONFIG_BT_L2CAP_TX_MTU=498`, `CONFIG_BT_BUF_ACL_RX_SIZE=502`).
- **Data Length Extension** (LL packets 251 bytes): `CONFIG_BT_CTLR_DATA_LENGTH_MAX=251`.
- **2M PHY** where both sides support it.
- **Connection interval** short (7.5-15 ms) during DFU; request it with a connection parameter
  update when DFU starts, relax afterwards.
- Write-without-response with flow control (SMP uses notifications/requests with a window;
  set the "number of buffers"/"memory alignment" options in the phone app).
Typical results: 10-20 KB/s untuned, 50-100+ KB/s tuned on modern phones.

## Robustness
- Resume: SMP image upload reports the offset; the client restarts from it after reconnecting.
  Don't erase the whole slot again on reconnect.
- Erase timing: erasing a large secondary slot at upload start can exceed BLE supervision
  timeout if done synchronously; let the stack erase incrementally
  (`CONFIG_IMG_ERASE_PROGRESSIVELY=y`).
- Power: phones may drop connections when the app backgrounds; keep the update screen in the
  foreground and handle disconnects as normal flow.
- Test-and-confirm: after reboot into the new image, confirm only after self-test passes, or
  MCUboot reverts.

## Security
- Require bonding/encryption before the SMP service accepts uploads, or use the SMP
  security/authentication extensions; an open DFU service lets anyone in radio range flash the
  device (the image signature prevents foreign images but not downgrades or DoS).
- Signed images verified by the bootloader, with anti-rollback counters.

## Verify
- [ ] Measured upload time for the full image on low-end and high-end phones.
- [ ] Kill the phone app mid-transfer, reconnect: upload resumes and completes.
- [ ] Unauthenticated connection cannot start an upload.
