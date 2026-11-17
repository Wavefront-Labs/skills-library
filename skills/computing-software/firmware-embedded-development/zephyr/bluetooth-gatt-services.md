---
id: computing-software.firmware-embedded-development.zephyr.bluetooth-gatt-services
name: bluetooth-gatt-services
category: computing-software
field: firmware-embedded-development
product: zephyr
tags: [zephyr-networking, zephyr-bluetooth-gatt, bt-gatt-service-define, bt-gatt-notify, ccc-descriptor, att-mtu, zephyr, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Define a custom GATT service in the Zephyr Bluetooth stack: BT_GATT_SERVICE_DEFINE, read/write callbacks, CCC and notifications, permissions and MTU sizing."
sources:
  - https://docs.zephyrproject.org/latest/services/connectivity/bluetooth/api/gatt.html
  - https://github.com/zephyrproject-rtos/zephyr/blob/main/include/zephyr/bluetooth/gatt.h
  - https://github.com/zephyrproject-rtos/zephyr/tree/main/samples/bluetooth/peripheral
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bluetooth GATT services

## Config
```
CONFIG_BT=y
CONFIG_BT_PERIPHERAL=y
CONFIG_BT_DEVICE_NAME="acme-sensor"
CONFIG_BT_L2CAP_TX_MTU=247        # larger ATT MTU for bigger notifications
CONFIG_BT_BUF_ACL_RX_SIZE=251
CONFIG_BT_BUF_ACL_TX_SIZE=251
CONFIG_BT_CTLR_DATA_LENGTH_MAX=251  # on-chip controller: data length extension
```

## Static service definition
```c
#include <zephyr/bluetooth/gatt.h>
#include <zephyr/bluetooth/uuid.h>

#define ACME_SVC_UUID  BT_UUID_128_ENCODE(0x6e400001, 0xb5a3, 0xf393, 0xe0a9, 0xe50e24dcca9e)
#define ACME_TEMP_UUID BT_UUID_128_ENCODE(0x6e400002, 0xb5a3, 0xf393, 0xe0a9, 0xe50e24dcca9e)
#define ACME_CFG_UUID  BT_UUID_128_ENCODE(0x6e400003, 0xb5a3, 0xf393, 0xe0a9, 0xe50e24dcca9e)
static const struct bt_uuid_128 svc_uuid  = BT_UUID_INIT_128(ACME_SVC_UUID);
static const struct bt_uuid_128 temp_uuid = BT_UUID_INIT_128(ACME_TEMP_UUID);
static const struct bt_uuid_128 cfg_uuid  = BT_UUID_INIT_128(ACME_CFG_UUID);

static int16_t temp_c100;
static uint8_t cfg_rate = 1;
static bool notify_on;

static ssize_t read_temp(struct bt_conn *c, const struct bt_gatt_attr *a,
                         void *buf, uint16_t len, uint16_t off)
{ return bt_gatt_attr_read(c, a, buf, len, off, &temp_c100, sizeof(temp_c100)); }

static ssize_t write_cfg(struct bt_conn *c, const struct bt_gatt_attr *a,
                         const void *buf, uint16_t len, uint16_t off, uint8_t flags)
{
    if (off) return BT_GATT_ERR(BT_ATT_ERR_INVALID_OFFSET);
    if (len != 1) return BT_GATT_ERR(BT_ATT_ERR_INVALID_ATTRIBUTE_LEN);
    cfg_rate = *(const uint8_t *)buf;
    return len;
}
static void temp_ccc_changed(const struct bt_gatt_attr *a, uint16_t value)
{ notify_on = (value == BT_GATT_CCC_NOTIFY); }

BT_GATT_SERVICE_DEFINE(acme_svc,
    BT_GATT_PRIMARY_SERVICE(&svc_uuid),                                   /* attrs[0] */
    BT_GATT_CHARACTERISTIC(&temp_uuid.uuid, BT_GATT_CHRC_READ | BT_GATT_CHRC_NOTIFY,
                           BT_GATT_PERM_READ, read_temp, NULL, NULL),     /* attrs[1], [2] */
    BT_GATT_CCC(temp_ccc_changed, BT_GATT_PERM_READ | BT_GATT_PERM_WRITE),/* attrs[3] */
    BT_GATT_CHARACTERISTIC(&cfg_uuid.uuid, BT_GATT_CHRC_WRITE,
                           BT_GATT_PERM_WRITE_ENCRYPT, NULL, write_cfg, NULL),
);
```

## Notifying
```c
if (notify_on) {
    int rc = bt_gatt_notify(NULL, &acme_svc.attrs[1], &temp_c100, sizeof(temp_c100));
    /* NULL conn = notify all peers that enabled notifications via the CCC; negative = error */
}
```
Attribute indices shift when you add entries. Look up by UUID with `bt_gatt_find_by_uuid()`
if the table changes often. Notification payload max = ATT_MTU - 3 (opcode and handle); the MTU
is negotiated per connection (`bt_gatt_get_mtu(conn)`), and the default MTU of 23 gives 20 bytes.
32-bit UUIDs are not supported in GATT; convert them to 128-bit.

## Permissions
`BT_GATT_PERM_READ_ENCRYPT` / `_WRITE_ENCRYPT` require encryption for access; `_READ_AUTHEN` /
`_WRITE_AUTHEN` require encryption using an authenticated link key.

## Verify
- [ ] nRF Connect (mobile) shows the service, reads, writes and receives notifications.
- [ ] Notification rate test: no -ENOMEM storms; app backs off when buffers are full.
- [ ] Encrypted characteristic rejects access before pairing.

## Checked

Checked 2026-10-25 against the Zephyr source tree (main, post-4.4; latest release v4.4.2): doc/services/connectivity/bluetooth/api/gatt.rst, include/zephyr/bluetooth/gatt.h and uuid.h, subsys/bluetooth/host/Kconfig.
Confirmed: `BT_GATT_SERVICE_DEFINE`, `BT_GATT_PRIMARY_SERVICE`, `BT_GATT_CHARACTERISTIC(uuid, props, perm, read, write, user_data)`, `BT_GATT_CCC(changed, perm)` with the `void (*)(const struct bt_gatt_attr *, uint16_t)` callback, write callback signature with `flags`, `BT_GATT_ERR`, `BT_GATT_CCC_NOTIFY`, the permission flags, `bt_gatt_notify` with NULL connection, `bt_gatt_find_by_uuid`, `bt_gatt_get_mtu`, `BT_UUID_128_ENCODE`, `BT_UUID_INIT_128`, `BT_DEVICE_NAME`; ATT_MTU - 3 payload; 32-bit UUIDs unsupported.

Method: documentation only; no commands were run.
