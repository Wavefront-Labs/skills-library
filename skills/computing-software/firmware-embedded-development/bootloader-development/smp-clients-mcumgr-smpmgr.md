---
id: computing-software.firmware-embedded-development.bootloader-development.smp-clients-mcumgr-smpmgr
name: smp-clients-mcumgr-smpmgr
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [smp-client, mcuboot, mcumgr-cli, smpmgr, image-test-confirm, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Drive MCUmgr/SMP from the host: mcumgr CLI and smpmgr connection strings for serial, BLE and UDP, image upload/list/test/confirm/reset, and common errors."
sources:
  - https://docs.zephyrproject.org/latest/services/device_mgmt/mcumgr.html
  - https://github.com/intercreate/smpmgr
  - https://github.com/apache/mynewt-mcumgr-cli
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SMP clients (mcumgr CLI and smpmgr)

The device side (Zephyr MCUmgr, NuttX, Mynewt) speaks SMP; these host tools upload images and
manage slots.

## mcumgr (Go, apache/mynewt-mcumgr-cli)
```sh
mcumgr --conntype ble --connstring 'peer_name=<DEVICE_NAME>' echo hello
mcumgr --conntype ble --connstring 'peer_name=<DEVICE_NAME>' image list       # current images
mcumgr --conntype ble --connstring 'peer_name=<DEVICE_NAME>' image upload <filename>
mcumgr --conntype ble --connstring 'peer_name=<DEVICE_NAME>' image test <image-hash>   # run on next boot
mcumgr --conntype ble --connstring 'peer_name=<DEVICE_NAME>' reset
mcumgr --conntype ble --connstring 'peer_name=<DEVICE_NAME>' image confirm    # make the swap permanent
```
The project README shows exactly this BLE sequence. Other transports use a different `--conntype`
and `--connstring`: see the tool's help and the Zephyr MCUmgr page.

## smpmgr (Python)
CLI for SMP over serial (UART or USB), BLE or UDP; its README recommends installing from PyPI with
`pipx`, and offers portable executables for Windows, Linux and macOS. It supports user plugins for
proprietary SMP groups (`--plugin-path`) and is built on the `smp` and `smpclient` libraries, which
you can use in test scripts. Run `smpmgr --help` for the transport and command syntax.

## Image states
Typical flow (from the mcumgr README): list, upload, `test` the new image hash, reset, list again
to check the new image runs, then `confirm` to make the swap permanent. MCUboot reverts an
unconfirmed test swap at the next boot.

## Troubleshooting
| Symptom | Cause |
|---|---|
| image uploaded but no swap after reset | not marked `test` or `confirm`; or MCUboot rejected the image (check its log) |
| wrong hash on `test` | use the hash shown by `image list` for the uploaded image |
| upload corrupted or stalls on a serial link | console or log output sharing the same UART as SMP (a common cause; check Zephyr's SMP transport settings) |

## Verify
- [ ] `image list` after reset shows the new version active; after confirm, `confirmed` flag set.
- [ ] Upload with a broken image (wrong key) never becomes active.

## Checked

2026-10-28. Confirmed in the apache/mynewt-mcumgr-cli README: `--conntype ble --connstring peer_name=...`, and the echo / image list / upload / test / reset / confirm sequence. Confirmed in the smpmgr README: serial, BLE and UDP transports, PyPI distribution with `pipx` recommended, `--plugin-path`, `smp` and `smpclient` libraries. MCUboot design page for test swap and revert.
Removed: `conn add` profile syntax, UDP/serial connection strings, smpmgr `--port`/`--ble` examples and subcommands, `rc=3`, `CONFIG_MCUMGR_TRANSPORT_NETBUF_SIZE`, MTU and timeout troubleshooting rows (none appear in the fetched pages).

Method: documentation only; no commands were run.
