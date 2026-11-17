---
id: computing-software.firmware-embedded-development.esp-idf.nimble-gatt-server
name: nimble-gatt-server
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-ble, nimble-gatt-server, ble-gatt-svc-def, access-callback, notifications, cccd, ble-gatts-notify-custom, nimble-port-freertos, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Build a BLE GATT server on ESP32 with NimBLE: service tables, access callbacks with mbufs, notifications and CCCD subscription tracking, and host task setup."
sources:
  - https://github.com/apache/mynewt-nimble/blob/master/nimble/host/include/host/ble_gatt.h
  - https://github.com/apache/mynewt-nimble/blob/master/nimble/host/include/host/ble_hs.h
  - https://github.com/apache/mynewt-nimble/blob/master/nimble/host/include/host/ble_hs_mbuf.h
  - https://github.com/apache/mynewt-nimble/blob/master/nimble/host/include/host/ble_uuid.h
  - https://github.com/apache/mynewt-nimble/blob/master/nimble/host/include/host/ble_att.h
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/bluetooth/nimble/index.rst
  - https://github.com/espressif/esp-idf/blob/master/components/bt/host/nimble/Kconfig.in
  - https://github.com/espressif/esp-idf/blob/master/examples/bluetooth/nimble/bleprph/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NimBLE GATT server on ESP32

**Goal:** custom BLE services (configuration, sensor data, commands) with the NimBLE host.

## Enable
Choose NimBLE as the Bluetooth host (`CONFIG_BT_HOST` choice, giving `CONFIG_BT_NIMBLE_ENABLED`);
tune `CONFIG_BT_NIMBLE_MAX_CONNECTIONS` and `CONFIG_BT_NIMBLE_ATT_PREFERRED_MTU`.

## Service table
```c
static uint16_t data_handle;
static const ble_uuid128_t svc_uuid = BLE_UUID128_INIT(/* 16 bytes, little-endian */);
static const ble_uuid128_t chr_uuid = BLE_UUID128_INIT(/* ... */);

static int chr_access(uint16_t conn, uint16_t attr, struct ble_gatt_access_ctxt *ctxt, void *arg) {
    switch (ctxt->op) {
    case BLE_GATT_ACCESS_OP_READ_CHR:
        return os_mbuf_append(ctxt->om, &g_value, sizeof g_value) ? BLE_ATT_ERR_INSUFFICIENT_RES : 0;
    case BLE_GATT_ACCESS_OP_WRITE_CHR: {
        uint16_t len = OS_MBUF_PKTLEN(ctxt->om);
        if (len != sizeof g_value) return BLE_ATT_ERR_INVALID_ATTR_VALUE_LEN;
        return ble_hs_mbuf_to_flat(ctxt->om, &g_value, sizeof g_value, NULL);
    }
    default: return BLE_ATT_ERR_UNLIKELY;
    }
}

static const struct ble_gatt_svc_def svcs[] = {
    { .type = BLE_GATT_SVC_TYPE_PRIMARY, .uuid = &svc_uuid.u,
      .characteristics = (struct ble_gatt_chr_def[]) {
        { .uuid = &chr_uuid.u, .access_cb = chr_access, .val_handle = &data_handle,
          .flags = BLE_GATT_CHR_F_READ | BLE_GATT_CHR_F_WRITE | BLE_GATT_CHR_F_NOTIFY },
        { 0 } } },
    { 0 } };
/* init: ble_svc_gap_init(); ble_svc_gatt_init(); ble_gatts_count_cfg(svcs); ble_gatts_add_svcs(svcs); */
```
Data arrives as **mbuf chains**, possibly fragmented: always copy with `ble_hs_mbuf_to_flat`,
never assume `ctxt->om->om_data` holds the whole value.

## Notifications
Track subscription in the GAP event handler (`BLE_GAP_EVENT_SUBSCRIBE`, `cur_notify`), then:
```c
struct os_mbuf *om = ble_hs_mbuf_from_flat(&sample, sizeof sample);
ble_gatts_notify_custom(conn_handle, data_handle, om);   /* consumes om */
```
Don't notify unsubscribed clients; keep the payload within the negotiated ATT MTU.

## Host task
```c
nimble_port_init();
ble_hs_cfg.sync_cb = on_sync;            /* start advertising here */
ble_hs_cfg.reset_cb = on_reset;
nimble_port_freertos_init(host_task);    /* host_task calls nimble_port_run() */
```
GATT callbacks run in the NimBLE host task: keep them short; post work to your own task.

## Gotchas
- 128-bit UUID macro byte order is little-endian (reverse of the string form).
- Characteristic security: add `BLE_GATT_CHR_F_WRITE_ENC`/`_AUTHEN` flags to require pairing.
- Changing the service table between firmware versions on bonded devices: clients may cache
  handles, so plan for the GATT Service Changed mechanism.

## Verify
- [ ] nRF Connect app can read, write and subscribe; notifications arrive at the expected rate.
- [ ] Fragmented long writes (> 20 bytes with MTU 23) are reassembled correctly.

## Checked
2026-10-26. ESP-IDF master (latest release v6.1, head 2026-10-23) and apache/mynewt-nimble master headers. Confirmed: NimBLE selection via CONFIG_BT_HOST, nimble_port_init and nimble_port_freertos_init sequence (ESP-IDF NimBLE page), BLE_UUID128_INIT takes little-endian bytes, ble_gatts_count_cfg/add_svcs, BLE_GATT_CHR_F_NOTIFY and WRITE_ENC/WRITE_AUTHEN flags, BLE_ATT_ERR_* constants, ble_hs_mbuf_to_flat/from_flat, ble_gatts_notify_custom, BLE_GAP_EVENT_SUBSCRIBE, ble_hs_cfg sync_cb/reset_cb, Kconfig MAX_CONNECTIONS and ATT_PREFERRED_MTU. Removed the unconfirmed 50 % RAM/flash saving, example MTU value and Service Changed default.
Method: documentation only; no commands were run.
