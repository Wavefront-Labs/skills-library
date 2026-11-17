---
id: computing-software.firmware-embedded-development.zephyr.bluetooth-att-mtu-and-l2cap-buffers
name: bluetooth-att-mtu-and-l2cap-buffers
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [bt-mtu, bt-l2cap-tx-mtu, bt-buf-acl-rx-size, bt-gatt-exchange-mtu, data-length-extension, ble-throughput, zephyr, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Raise Zephyr BLE throughput: ATT MTU exchange, L2CAP and ACL buffer sizes, data length extension, buffer counts, and the Kconfig values that must agree with each other."
sources:
  - https://docs.zephyrproject.org/latest/services/connectivity/bluetooth/api/gatt.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/bluetooth/host/Kconfig.l2cap
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/bluetooth/common/Kconfig
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/subsys/bluetooth/host/Kconfig.gatt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bluetooth ATT MTU and L2CAP buffers

Default ATT MTU is 23 bytes (20 bytes of notification payload). Larger MTU plus data length
extension (DLE) and 2M PHY gives big throughput gains.

## Matching Kconfig values (247-byte MTU example)
```
CONFIG_BT_L2CAP_TX_MTU=247              # ATT MTU we can send
CONFIG_BT_BUF_ACL_RX_SIZE=251           # = MTU + 4 (L2CAP header); limits RX MTU
CONFIG_BT_BUF_ACL_TX_SIZE=251           # controller ACL payload (DLE max 251)
CONFIG_BT_CTLR_DATA_LENGTH_MAX=251      # Zephyr LL controller; vendor controllers have their own
CONFIG_BT_USER_DATA_LEN_UPDATE=y
CONFIG_BT_USER_PHY_UPDATE=y
CONFIG_BT_BUF_ACL_TX_COUNT=10           # in-flight packets
CONFIG_BT_L2CAP_TX_BUF_COUNT=10
CONFIG_BT_ATT_TX_COUNT=10               # default: BT_BUF_ACL_TX_COUNT
```
`CONFIG_BT_CONN_TX_MAX` was deprecated in Zephyr 4.2 and removed in 4.5; the number of pending TX
buffers with a callback follows `CONFIG_BT_BUF_ACL_TX_COUNT`.
Rule of thumb: `BUF_ACL_RX_SIZE = L2CAP_TX_MTU + 4` (4-byte L2CAP header); the stock Kconfig
defaults follow it (with SMP: MTU 65, RX size 69; with EATT: 66 and 70). The controller's
`BT_CTLR_DATA_LENGTH_MAX` has range 27 to 251 and defaults to `BT_BUF_ACL_RX_SIZE` when that is 251
or less.

## Exchange the MTU (client side)
```c
static void mtu_cb(struct bt_conn *conn, uint8_t err, struct bt_gatt_exchange_params *p)
{
    printk("MTU %u\n", bt_gatt_get_mtu(conn));
}
static struct bt_gatt_exchange_params xp = { .func = mtu_cb };
bt_gatt_exchange_mtu(conn, &xp);
```
As a peripheral, the central (phone) usually initiates; Zephyr responds with its RX MTU.
`CONFIG_BT_GATT_AUTO_UPDATE_MTU` (depends on `CONFIG_BT_GATT_CLIENT`) sends the MTU exchange
request automatically on connect. Notification payload max = ATT_MTU - 3 (opcode and handle);
check `bt_gatt_get_mtu()` before sizing notifications.

## Data length and PHY
```c
bt_conn_le_data_len_update(conn, BT_LE_DATA_LEN_PARAM_MAX);
bt_conn_le_phy_update(conn, BT_CONN_LE_PHY_PARAM_2M);
```
Without DLE, a 247-byte ATT PDU is fragmented into 27-byte link-layer packets (works, slower).

## Throughput levers
- Connection interval and how many packets per event the controller sends (more TX buffers help).
- Use notifications (no ACK at ATT) with a completion callback (`bt_gatt_notify_cb` +
  `.func`) to keep the pipeline full without overflowing buffers; a negative return means the
  buffers are exhausted, so wait for completions.
- The 2M PHY raises the air rate; the Coded PHY lowers it.

## Gotchas
- Raising MTU without raising buffer counts can lower throughput (only one packet in flight).
- RAM grows with size times count of each pool; check `ram_report`.
- The peer may cap MTU and data length; measure with the real peer.

## Verify
- [ ] Log shows negotiated MTU, DLE (tx/rx octets) and PHY after connection.
- [ ] Throughput measured with the `throughput` sample or app counters against the target.

## Checked

Checked 2026-10-25 against the Zephyr source tree (main, post-4.4; latest release v4.4.2): subsys/bluetooth/host/Kconfig.l2cap, Kconfig.gatt, Kconfig, subsys/bluetooth/common/Kconfig, subsys/bluetooth/controller/Kconfig, include/zephyr/bluetooth/gatt.h and conn.h, and the 4.5 migration guide.
Confirmed: default ATT MTU 23 (`BT_L2CAP_TX_MTU` default); the MTU + 4 relation in the stock defaults; `BT_BUF_ACL_TX_SIZE`, `BT_BUF_ACL_RX_SIZE`, `BT_BUF_ACL_TX_COUNT`, `BT_L2CAP_TX_BUF_COUNT`, `BT_ATT_TX_COUNT`, `BT_USER_DATA_LEN_UPDATE`, `BT_USER_PHY_UPDATE` exist; data-length range 27-251; `bt_gatt_exchange_mtu`, `bt_gatt_get_mtu`, `bt_gatt_notify_cb`, `bt_conn_le_data_len_update`, `bt_conn_le_phy_update`, `BT_LE_DATA_LEN_PARAM_MAX`, `BT_CONN_LE_PHY_PARAM_2M`; notification payload ATT_MTU - 3; `BT_GATT_AUTO_UPDATE_MTU` depends on `BT_GATT_CLIENT`.

Method: documentation only; no commands were run.
