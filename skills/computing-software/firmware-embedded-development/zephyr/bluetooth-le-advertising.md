---
id: computing-software.firmware-embedded-development.zephyr.bluetooth-le-advertising
name: bluetooth-le-advertising
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr-networking, zephyr-ble-advertising, bt-le-adv-start, advertising-data, scan-response, extended-advertising, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Advertise from a Zephyr BLE peripheral: AD and scan-response payloads, connectable parameters, restarting after disconnect, and extended advertising sets."
sources:
  - https://docs.zephyrproject.org/latest/services/connectivity/bluetooth/api/gap.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/bluetooth/bluetooth.h
  - https://github.com/zephyrproject-rtos/zephyr/tree/main/samples/bluetooth/peripheral
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bluetooth LE advertising

## Legacy connectable advertising
```c
#include <zephyr/bluetooth/bluetooth.h>
#include <zephyr/bluetooth/conn.h>

static const struct bt_data ad[] = {
    BT_DATA_BYTES(BT_DATA_FLAGS, (BT_LE_AD_GENERAL | BT_LE_AD_NO_BREDR)),
    BT_DATA(BT_DATA_NAME_COMPLETE, CONFIG_BT_DEVICE_NAME, sizeof(CONFIG_BT_DEVICE_NAME) - 1),
};
static const struct bt_data sd[] = {      /* scan response: sent only to active scanners */
    BT_DATA_BYTES(BT_DATA_UUID128_ALL, BT_UUID_128_ENCODE(0x6e400001, 0xb5a3, 0xf393,
                                                          0xe0a9, 0xe50e24dcca9e)),
};

static void adv_start(void)
{
    int err = bt_le_adv_start(BT_LE_ADV_CONN_FAST_1, ad, ARRAY_SIZE(ad), sd, ARRAY_SIZE(sd));
    if (err) LOG_ERR("adv start %d", err);
}

int main(void)
{
    bt_enable(NULL);
    if (IS_ENABLED(CONFIG_SETTINGS)) settings_load();   /* identity + bonds before advertising */
    adv_start();
}
```
Legacy AD and scan response are each limited to 31 bytes (`BT_GAP_ADV_MAX_ADV_DATA_LEN`), and each
field costs 2 bytes of length/type.
A 128-bit UUID (18 bytes) plus flags (3) leaves 10 bytes; put the UUID in the scan response and
a short name in AD, or shorten the name (`BT_DATA_NAME_SHORTENED`).

## Parameters
Custom interval and options:
```c
#define ADV_PARAM BT_LE_ADV_PARAM(BT_LE_ADV_OPT_CONN, \
        BT_GAP_ADV_SLOW_INT_MIN, BT_GAP_ADV_SLOW_INT_MAX, NULL)   /* 1 s - 1.2 s */
```
`BT_GAP_ADV_FAST_INT_MIN_2` is 100 ms. `BT_LE_ADV_CONN_FAST_1` is the GAP-recommended set for
user-initiated advertising; the header notes that a longer interval saves battery at the cost of
responsiveness and should be entered after a timeout. Non-connectable beacons:
`BT_LE_ADV_NCONN`.

## Restart after disconnect
When a connection is made the connectable advertiser is no longer running, so start it again.
The `recycled` callback is documented as the event to listen for before starting a new
connectable advertiser, once a connection object has returned to the pool:
```c
static void recycled(void) { adv_start(); }
BT_CONN_CB_DEFINE(conn_cbs) = { .recycled = recycled };
```
Restarting from `disconnected` can fail with -ENOMEM (no free connection object) because the
stack still holds a reference to the old connection; `recycled` avoids that.

## Updating payload
`bt_le_adv_update_data(ad, n, sd, m)` updates the advertising and scan response data of the
running advertiser. A sensor value can go in manufacturer data (`BT_DATA_MANUFACTURER_DATA`,
with a 2-byte company ID first).

## Extended advertising
`CONFIG_BT_EXT_ADV=y` (needs controller support): `bt_le_ext_adv_create(param, &cb, &adv)`,
`bt_le_ext_adv_set_data`, `bt_le_ext_adv_start(adv, BT_LE_EXT_ADV_START_DEFAULT)`. It enables
multiple advertising sets (`CONFIG_BT_EXT_ADV_MAX_ADV_SET`, default 1), larger advertising data
(up to `BT_GAP_ADV_MAX_EXT_ADV_DATA_LEN` = 1650 bytes, as limited by the controller) and the LE
Coded PHY. Legacy scanners do not receive extended advertising packets; keep a legacy set if you
need to reach them.

## Verify
- [ ] Device visible in a phone scanner with correct name and UUID; payload fits (no -EINVAL from start).
- [ ] Connect, disconnect, repeat 100x: advertising always resumes.
- [ ] Measured average current matches the interval budget.

## Checked

Checked 2026-10-25 against the Zephyr source tree (main, post-4.4; latest release v4.4.2): include/zephyr/bluetooth/bluetooth.h, gap.h, data.h, conn.h and subsys/bluetooth/Kconfig.adv.
Confirmed: `bt_le_adv_start` signature and its -ENOMEM return; `BT_LE_ADV_CONN_FAST_1`, `BT_LE_ADV_NCONN`, `BT_LE_ADV_PARAM`; `BT_GAP_ADV_FAST_INT_MIN_2` = 0x00a0 (100 ms), `BT_GAP_ADV_SLOW_INT_MIN`/`MAX` = 0x0640/0x0780 (1 s to 1.2 s); `BT_DATA`, `BT_DATA_BYTES`; 31-byte legacy limit; `BT_GAP_ADV_MAX_EXT_ADV_DATA_LEN` = 1650; `bt_le_adv_update_data`; `bt_le_ext_adv_create`/`set_data`/`start` and `BT_LE_EXT_ADV_START_DEFAULT`; `BT_EXT_ADV` and `BT_EXT_ADV_MAX_ADV_SET`; the `recycled` callback guidance; legacy scanners not receiving extended advertising.

Method: documentation only; no commands were run.
