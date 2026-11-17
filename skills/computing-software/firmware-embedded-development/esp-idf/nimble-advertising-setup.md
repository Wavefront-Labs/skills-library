---
id: computing-software.firmware-embedded-development.esp-idf.nimble-advertising-setup
name: nimble-advertising-setup
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-ble, nimble-advertising, ble-gap-adv-start, adv-fields, scan-response, device-name, restart-on-disconnect, own-addr-type, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Advertise an ESP32 NimBLE peripheral correctly: adv fields vs scan response within 31 bytes, address type, intervals, and restarting after disconnect or connection failure."
sources:
  - https://github.com/apache/mynewt-nimble/blob/master/nimble/host/include/host/ble_gap.h
  - https://github.com/apache/mynewt-nimble/blob/master/nimble/host/include/host/ble_hs_adv.h
  - https://github.com/apache/mynewt-nimble/blob/master/nimble/host/include/host/ble_hs_id.h
  - https://github.com/espressif/esp-idf/blob/master/components/bt/host/nimble/Kconfig.in
  - https://github.com/espressif/esp-idf/blob/master/examples/bluetooth/nimble/bleprph/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NimBLE advertising setup (ESP-IDF)

**Goal:** a peripheral that phones find with the right name and service UUID, and that is
advertising again whenever it isn't connected.

## Fields within 31 bytes
Legacy advertising data is limited to 31 bytes; a 128-bit UUID takes 18 and the flags 3,
leaving ~10 for the name. Split: UUID + flags in the advertisement, full name in the **scan
response**.
```c
static void advertise(void) {
    struct ble_hs_adv_fields f = {0};
    f.flags = BLE_HS_ADV_F_DISC_GEN | BLE_HS_ADV_F_BREDR_UNSUP;
    f.uuids128 = (ble_uuid128_t[]){ svc_uuid }; f.num_uuids128 = 1; f.uuids128_is_complete = 1;
    ble_gap_adv_set_fields(&f);

    struct ble_hs_adv_fields rsp = {0};
    const char *name = ble_svc_gap_device_name();
    rsp.name = (uint8_t *)name; rsp.name_len = strlen(name); rsp.name_is_complete = 1;
    rsp.tx_pwr_lvl_is_present = 1; rsp.tx_pwr_lvl = BLE_HS_ADV_TX_PWR_LVL_AUTO;
    ble_gap_adv_rsp_set_fields(&rsp);

    struct ble_gap_adv_params p = {0};
    p.conn_mode = BLE_GAP_CONN_MODE_UND;     /* connectable */
    p.disc_mode = BLE_GAP_DISC_MODE_GEN;
    p.itvl_min = BLE_GAP_ADV_ITVL_MS(100); p.itvl_max = BLE_GAP_ADV_ITVL_MS(150);
    ble_gap_adv_start(own_addr_type, NULL, BLE_HS_FOREVER, &p, gap_event, NULL);
}
```
`ble_gap_adv_set_fields` returns `BLE_HS_EMSGSIZE` when the data exceeds 31 bytes: check it.

## Address type
In `sync_cb`: `ble_hs_id_infer_auto(0, &own_addr_type)` picks public or static random address.
For privacy use a resolvable private address (`BLE_OWN_ADDR_RPA_RANDOM_DEFAULT`).

## Restarting
Advertising stops when a connection is made. Restart in the GAP event handler (the header warns
that `ble_gap_adv_stop()` followed directly by `ble_gap_adv_start()` is unreliable when called from
the host task context; start from a separate event context):
- `BLE_GAP_EVENT_DISCONNECT` -> `advertise()`
- `BLE_GAP_EVENT_CONNECT` with non-zero status (failed connection) -> `advertise()`
- `BLE_GAP_EVENT_ADV_COMPLETE` (duration expired) -> slow advertising or sleep
Forgetting the failed-connect case can leave the device not advertising.

## Extended advertising
`CONFIG_BT_NIMBLE_EXT_ADV` (needs BLE 5 support, default off) enables the `ble_gap_ext_adv_*`
APIs for larger payloads and coded PHY; see the nimble-extended-advertising skill.

## Verify
- [ ] Phone scanner shows name, UUID, TX power.
- [ ] After 100 connect/disconnect cycles (and a forced connect failure) the device still advertises.

## Checked
2026-10-26. ESP-IDF master (latest release v6.1, head 2026-10-23) and apache/mynewt-nimble master headers. Confirmed signatures and names: ble_gap_adv_set_fields, ble_gap_adv_rsp_set_fields (BLE_HS_EMSGSIZE when too large), ble_gap_adv_start arguments, struct ble_gap_adv_params fields conn_mode/disc_mode, BLE_GAP_ADV_ITVL_MS, BLE_HS_FOREVER, BLE_GAP_EVENT_ADV_COMPLETE, ble_hs_id_infer_auto(privacy, &type), BLE_OWN_ADDR_RPA_RANDOM_DEFAULT, BLE_HS_ADV_TX_PWR_LVL_AUTO; CONFIG_BT_NIMBLE_EXT_ADV default n, depends on BLE 5 support. Removed the unconfirmed claim that legacy calls stop working with extended advertising.
Method: documentation only; no commands were run.
