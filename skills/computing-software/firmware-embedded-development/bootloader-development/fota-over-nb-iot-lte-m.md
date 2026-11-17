---
id: computing-software.firmware-embedded-development.bootloader-development.fota-over-nb-iot-lte-m
name: fota-over-nb-iot-lte-m
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [nb-iot-fota, firmware-transport, lte-m, psm-edrx-update, modem-firmware-update, firmware-embedded-development]
level: advanced
status: draft
description: "Plan firmware updates over NB-IoT and LTE-M: throughput and latency limits, data cost, PSM/eDRX scheduling, delta images, resume, and updating the cellular modem firmware."
sources:
  - https://www.gsma.com/iot/mobile-iot-modules/
  - https://docs.nordicsemi.com/bundle/ncs-latest/page/nrf/libraries/dfu/fota_download.html
  - https://www.3gpp.org/technologies/nb-iot
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# FOTA over NB-IoT and LTE-M

## Link realities
| | NB-IoT | LTE-M |
|---|---|---|
| Practical throughput | ~20-60 kbit/s down, often less at poor coverage (CE levels) | ~200-800 kbit/s |
| Latency | 1-10 s RTT possible | 50-200 ms |
| Mobility | limited (no connected-mode handover) | yes |
A 500 KB image over NB-IoT can take 10+ minutes of radio-on time at the cell edge: significant
battery energy (100s of mAh on a weak link) and data cost on per-MB plans.

## Reduce bytes
- **Delta updates** (e.g. detools, JojoDiff-based, vendor delta FOTA for modems): often 5-20% of
  the full image for minor releases.
- Compress full images (LZMA/heatshrink) if the bootloader can decompress.
- Split assets (certificates, configs) from code so small changes don't ship the whole image.

## Transport choice
- **CoAP block-wise over DTLS/UDP**: lowest overhead, tolerates NAT timeouts with resumption
  (DTLS Connection ID, RFC 9146, avoids re-handshakes after NAT rebinding).
- **HTTPS with Range requests**: simpler infrastructure, higher overhead (TCP + TLS handshakes,
  which hurt at multi-second RTT). Use TLS session resumption.
- **LwM2M Object 5** if the device is LwM2M-managed.

## Scheduling around power-saving modes
- Devices in PSM are unreachable; the server can't push. Use a pull model: the device checks for
  updates on its regular uplink and the response carries "update available".
- During download, request a temporary exit from PSM/eDRX (or shorter timers via
  `AT+CPSMS`/`AT+CEDRXS`), then restore the low-power configuration after.
- Avoid peak hours / respect operator guidance for fleet-wide campaigns (staggered schedules);
  some operators throttle large transfers.

## Resilience
- Persist progress; resume across coverage loss and resets (see resumable downloads).
- Check battery/supply before starting and before the swap; abort on low battery.
- Timeouts generous enough for CE level 2 (seconds per block).

## Modem firmware
The cellular module has its own firmware (e.g. nRF91 modem, Quectel, u-blox), updated via
vendor-specific delta FOTA (AT commands like `AT+QFOTADL`, nRF `nrf_modem_delta_dfu`) or full
updates through the host MCU. Carrier certification may restrict which modem versions are allowed.

## Verify
- [ ] Field-like test (network emulator or poor-coverage site): full and delta updates complete with resume; energy per update measured.
- [ ] Device returns to its PSM/eDRX configuration after the update.
