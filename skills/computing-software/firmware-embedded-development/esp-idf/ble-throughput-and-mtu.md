---
id: computing-software.firmware-embedded-development.esp-idf.ble-throughput-and-mtu
name: ble-throughput-and-mtu
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-ble, ble-throughput, att-mtu, data-length-extension, ble-2m-phy, connection-interval, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Maximise ESP32 BLE data throughput with ATT MTU exchange, data length extension, 2M PHY, connection interval choice and notification batching in NimBLE."
sources:
  - https://github.com/apache/mynewt-nimble/blob/master/nimble/host/include/host/ble_gap.h
  - https://github.com/espressif/esp-idf/tree/master/examples/bluetooth/nimble/throughput_app
  - https://github.com/espressif/esp-idf/blob/master/components/bt/host/nimble/Kconfig.in
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BLE throughput and MTU

Throughput = payload per connection event x events per second. Each lever:

## 1. ATT MTU
```c
ble_att_set_preferred_mtu(517);                 /* CONFIG_BT_NIMBLE_ATT_PREFERRED_MTU, default 256 */
ble_gattc_exchange_mtu(conn, on_mtu, NULL);     /* central initiates; peripheral responds */
/* BLE_GAP_EVENT_MTU gives the negotiated value; payload per notify = mtu - 3 */
```
The negotiated MTU is the smaller of both sides' values; phones choose their own.

## 2. Data length extension (LL packet up to 251 bytes)
```c
ble_gap_set_data_len(conn, 251, 2120);          /* tx octets, tx time us */
```

## 3. 2M PHY (needs a BLE 5 chip with `CONFIG_BT_NIMBLE_50_FEATURE_SUPPORT` and `CONFIG_BT_NIMBLE_LL_CFG_FEAT_LE_2M_PHY`)
```c
ble_gap_set_prefered_le_phy(conn, BLE_GAP_LE_PHY_2M_MASK, BLE_GAP_LE_PHY_2M_MASK, BLE_GAP_LE_PHY_CODED_ANY);
```

## 4. Connection interval
```c
struct ble_gap_upd_params u = { .itvl_min = 6, .itvl_max = 12,  /* 7.5-15 ms in 1.25 ms units */
    .latency = 0, .supervision_timeout = 400 };
ble_gap_update_params(conn, &u);
```
Short intervals are not automatically faster: the number of packets per event matters. The central decides whether to accept the requested parameters, so log the values actually in effect.

## 5. Keep the pipe full
Use notifications (no ATT ack) and queue several before the event ends. When
`ble_gatts_notify_custom` returns `BLE_HS_ENOMEM`, the mbuf pool is exhausted: wait for
`BLE_GAP_EVENT_NOTIFY_TX` completions, then continue. Raise `CONFIG_BT_NIMBLE_MSYS_1_BLOCK_COUNT` (default 24 or 12 depending on the controller).
Indications and write-with-response cost one round trip each, so they carry far less per connection interval.

## Throughput numbers
Measure on your own hardware pair; the ESP-IDF `throughput_app` example is the reference for doing so.

## Verify
- [ ] Log negotiated MTU, data length, PHY and interval on each connection.
- [ ] Measure bytes/s over 60 s with a counter on both sides; no dropped sequence numbers.

## Checked

2026-10-25, against the ESP-IDF documentation source (espressif/esp-idf docs/en, master, v6.1 release period). Confirmed from the NimBLE headers and ESP-IDF NimBLE Kconfig: ble_att_set_preferred_mtu, ble_gattc_exchange_mtu, ble_gap_set_data_len, ble_gap_set_prefered_le_phy (API spelling), ble_gap_update_params, BLE_GAP_EVENT_MTU and NOTIFY_TX, BLE_HS_ENOMEM from notify, ATT_PREFERRED_MTU default 256, MSYS_1_BLOCK_COUNT, 2M PHY Kconfig gates. Removed the unconfirmed throughput figures, iOS/Android connection-interval and MTU behaviour, per-chip PHY list and 27-byte fragment claim.
Method: documentation only; no commands were run.
