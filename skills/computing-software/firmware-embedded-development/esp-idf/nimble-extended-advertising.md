---
id: computing-software.firmware-embedded-development.esp-idf.nimble-extended-advertising
name: nimble-extended-advertising
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-ble, nimble-extended-advertising, ble5-advertising, periodic-advertising, coded-phy, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Use BLE 5 extended and periodic advertising with NimBLE on ESP32-C3/S3/C6: multiple advertising sets, large payloads, coded PHY long range."
sources:
  - https://github.com/apache/mynewt-nimble/blob/master/nimble/host/include/host/ble_gap.h
  - https://github.com/espressif/esp-idf/blob/master/components/bt/host/nimble/Kconfig.in
  - https://github.com/espressif/esp-idf/blob/master/examples/bluetooth/nimble/ble_multi_adv/README.md
  - https://github.com/espressif/esp-idf/blob/master/examples/bluetooth/nimble/ble_periodic_adv/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NimBLE extended advertising

Requires a target with BLE 5 support (`CONFIG_BT_NIMBLE_50_FEATURE_SUPPORT`, which depends on
`SOC_BLE_50_SUPPORTED`) and `CONFIG_BT_NIMBLE_EXT_ADV=y` (default off). Use the
`ble_gap_ext_adv_*` API for extended advertising sets.

## One advertising set
```c
struct ble_gap_ext_adv_params p = {0};
p.connectable = 1;
p.own_addr_type = BLE_OWN_ADDR_PUBLIC;
p.primary_phy = BLE_HCI_LE_PHY_1M;
p.secondary_phy = BLE_HCI_LE_PHY_2M;
p.sid = 0;
p.itvl_min = p.itvl_max = BLE_GAP_ADV_ITVL_MS(200);
ble_gap_ext_adv_configure(0 /* instance */, &p, NULL, gap_cb, NULL);

struct os_mbuf *data = os_msys_get_pkthdr(0, 0);
os_mbuf_append(data, adv_bytes, adv_len);         /* Kconfig: extended adv data must not exceed 1650 */
ble_gap_ext_adv_set_data(0, data);
ble_gap_ext_adv_start(0, 0 /* forever */, 0);
```

## Long range (coded PHY)
`p.primary_phy = BLE_HCI_LE_PHY_CODED; p.secondary_phy = BLE_HCI_LE_PHY_CODED;` selects the
coded PHY (`CONFIG_BT_NIMBLE_LL_CFG_FEAT_LE_CODED_PHY`, default y). The scanner must scan on coded
PHY too (`ble_gap_ext_disc` with `coded_params`), and the scanner hardware must support it.

## Multiple sets
Set `CONFIG_BT_NIMBLE_MAX_EXT_ADV_INSTANCES` (range 0 to 4); give each instance a distinct SID and, for
privacy or beacons, a random address via `ble_gap_ext_adv_set_addr`.

## Periodic advertising
`CONFIG_BT_NIMBLE_ENABLE_PERIODIC_ADV` (default y with BLE 5); the instance must be a
non-anonymous, non-connectable, non-scannable extended set, then
`ble_gap_periodic_adv_configure/set_data/start`. Scanners sync with `ble_gap_periodic_adv_sync_create`
and receive data without scanning continuously: good for broadcast sensor data.

## Compatibility
Legacy scanners (older phones) only see legacy PDUs. If you must reach them, run an extra
instance with `p.legacy_pdu = 1` and payload at most 31 bytes.

## Verify
- [ ] nRF Connect on a BLE 5 phone shows the extended set with the full payload.
- [ ] Legacy instance visible to an older scanner when required.
- [ ] Coded PHY range test logged at distance.

## Checked
2026-10-26. ESP-IDF master (latest release v6.1, head 2026-10-23) and apache/mynewt-nimble master headers. Confirmed: struct ble_gap_ext_adv_params fields (connectable, scannable, legacy_pdu, primary_phy, secondary_phy, sid, itvl), ble_gap_ext_adv_configure/set_data/start/set_addr signatures, periodic advertising constraints, ble_gap_periodic_adv_sync_create; Kconfig: EXT_ADV default n and depends on BLE 5, MAX_EXT_ADV_INSTANCES range 0-4, ENABLE_PERIODIC_ADV, 1650 limit, coded PHY option. Wrong: scanner param name coded_scan_params (it is coded_params). Removed chip list, 4x range, phone support and "legacy calls unavailable" claims.
Method: documentation only; no commands were run.
