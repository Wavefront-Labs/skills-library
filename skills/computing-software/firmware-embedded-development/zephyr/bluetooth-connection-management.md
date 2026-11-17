---
id: computing-software.firmware-embedded-development.zephyr.bluetooth-connection-management
name: bluetooth-connection-management
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr-bt-conn, bt-conn-cb-define, bt-conn-ref, bt-conn-le-param-update, bt-conn-set-security, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Manage Zephyr Bluetooth LE connections: connection callbacks, reference counting, connection parameter updates, security levels and pairing, and disconnect handling."
sources:
  - https://docs.zephyrproject.org/latest/services/connectivity/bluetooth/api/connection_mgmt.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/bluetooth/conn.h
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/bluetooth/host/Kconfig.gatt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bluetooth connection management

## Callbacks
```c
#include <zephyr/bluetooth/conn.h>

static struct bt_conn *current;

static void connected(struct bt_conn *conn, uint8_t err)
{
    if (err) { printk("connect failed 0x%02x\n", err); return; }
    current = bt_conn_ref(conn);                /* keep a reference while you use it */
    bt_conn_set_security(conn, BT_SECURITY_L2); /* encrypt (pairing if needed) */
}

static void disconnected(struct bt_conn *conn, uint8_t reason)
{
    printk("disconnected 0x%02x\n", reason);    /* BT_HCI_ERR_* reason */
    if (current == conn) { bt_conn_unref(current); current = NULL; }
    /* restart advertising here or in recycled() */
}

static void le_param_updated(struct bt_conn *conn, uint16_t interval, uint16_t latency, uint16_t timeout)
{
    printk("interval %u.%02u ms latency %u timeout %u ms\n",
           interval * 125 / 100, (interval * 125) % 100, latency, timeout * 10);
}

static void security_changed(struct bt_conn *conn, bt_security_t level, enum bt_security_err err) { }

BT_CONN_CB_DEFINE(conn_cbs) = {
    .connected = connected,
    .disconnected = disconnected,
    .le_param_updated = le_param_updated,
    .security_changed = security_changed,
    .recycled = adv_restart,                     /* connection object freed: safe to advertise again */
};
```

## Reference counting
`connected` gives you a borrowed pointer. Call `bt_conn_ref` to keep it beyond the callback
and `bt_conn_unref` exactly once when done. `bt_conn_ref` returns NULL if the reference count is already zero. A leaked reference keeps the
connection object allocated, so the `CONFIG_BT_MAX_CONN` slots run out and starting a connectable
advertiser or a new connection can fail. The stack still holds one reference during
`disconnected`, so restart connectable advertising from `recycled` (called when a connection
object returns to the pool; no guarantee a slot is still free) instead.

## Connection parameters
```c
struct bt_le_conn_param p = BT_LE_CONN_PARAM_INIT(24, 40, 0, 400);  /* 30-50 ms, latency 0, 4 s timeout */
bt_conn_le_param_update(conn, &p);
```
- Units: interval 1.25 ms, timeout 10 ms.
- Peripheral preferred params: `CONFIG_BT_PERIPHERAL_PREF_MIN_INT` (default 24, in 1.25 ms
  units) and the matching MAX/LATENCY/TIMEOUT options, under `CONFIG_BT_GAP_PERIPHERAL_PREF_PARAMS`.
  `CONFIG_BT_GAP_AUTO_UPDATE_CONN_PARAMS` (default y, peripheral role) sends a parameter update
  request after the GAP-recommended 5 seconds of connection.
- The central decides: it may reject or alter a request, so check the `le_param_updated`
  callback for the parameters actually in use.
- PHY and data length: `bt_conn_le_phy_update` (2M PHY), `bt_conn_le_data_len_update`.

## Security
| Level | Meaning |
|---|---|
| `BT_SECURITY_L1` | no encryption and no authentication |
| `BT_SECURITY_L2` | encryption, no authentication (no MITM) |
| `BT_SECURITY_L3` | encryption and authentication (MITM) |
| `BT_SECURITY_L4` | authenticated Secure Connections and 128-bit key |
Pairing callbacks via `bt_conn_auth_cb_register()`. `CONFIG_BT_SETTINGS` (depends on
`CONFIG_SETTINGS`) stores the Bluetooth state, such as pairing keys, persistently in flash;
load it with `settings_load()` after `bt_enable()`.

## Disconnect
`bt_conn_disconnect(conn, BT_HCI_ERR_REMOTE_USER_TERM_CONN)`.

## Verify
- [ ] Repeated connect/disconnect cycles (hundreds) never exhaust connection slots.
- [ ] Negotiated params logged and acceptable for power/latency.
- [ ] Bonds persist across reboot.

## Checked

Checked 2026-10-25 against the Zephyr source tree (main, post-4.4; latest release v4.4.2): include/zephyr/bluetooth/conn.h and subsys/bluetooth/host/Kconfig, Kconfig.gatt.
Confirmed: `BT_CONN_CB_DEFINE` and the `connected`, `disconnected`, `recycled`, `le_param_updated`, `security_changed` callbacks; `bt_conn_ref` (NULL at zero count) and `bt_conn_unref`; `BT_LE_CONN_PARAM_INIT`; `bt_conn_le_param_update`, `bt_conn_set_security`, `bt_conn_disconnect`, `bt_conn_auth_cb_register`; security level meanings; `BT_PERIPHERAL_PREF_MIN_INT` default 24 and `BT_GAP_AUTO_UPDATE_CONN_PARAMS` (default y, 5 s); `BT_SETTINGS` depends on `SETTINGS`; `BT_MAX_CONN`.

Method: documentation only; no commands were run.
