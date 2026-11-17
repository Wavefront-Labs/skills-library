---
id: computing-software.firmware-embedded-development.esp-idf.nimble-central-gatt-client
name: nimble-central-gatt-client
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-ble, nimble-central, gatt-client, ble-gap-connect, service-discovery, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Build an ESP-IDF NimBLE central: scan, filter and connect to a peripheral, discover services and characteristics, read, write and subscribe to notifications."
sources:
  - https://github.com/apache/mynewt-nimble/blob/master/nimble/host/include/host/ble_gap.h
  - https://github.com/apache/mynewt-nimble/blob/master/nimble/host/include/host/ble_gatt.h
  - https://github.com/apache/mynewt-nimble/blob/master/nimble/host/include/host/ble_hs_adv.h
  - https://github.com/apache/mynewt-nimble/blob/master/nimble/host/include/host/ble_hs_mbuf.h
  - https://github.com/espressif/esp-idf/blob/master/examples/bluetooth/nimble/blecent/README.md
  - https://github.com/espressif/esp-idf/blob/master/components/bt/host/nimble/Kconfig.in
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NimBLE central and GATT client

Reference implementation: `examples/bluetooth/nimble/blecent` with the `peer.c` helper in
`examples/bluetooth/nimble/common/nimble_central_utils`, which caches discovered services. Reuse
it rather than writing discovery bookkeeping from scratch.

## Scan and connect
```c
static int gap_cb(struct ble_gap_event *ev, void *arg);

static void scan(void) {
    struct ble_gap_disc_params p = { .passive = 0, .filter_duplicates = 1, .itvl = 0x50, .window = 0x30 };
    ble_gap_disc(BLE_OWN_ADDR_PUBLIC, 10000 /* ms */, &p, gap_cb, NULL);
}

static int gap_cb(struct ble_gap_event *ev, void *arg) {
    switch (ev->type) {
    case BLE_GAP_EVENT_DISC: {
        struct ble_hs_adv_fields f;
        ble_hs_adv_parse_fields(&f, ev->disc.data, ev->disc.length_data);
        if (adv_has_uuid(&f, &MY_SVC_UUID)) {
            ble_gap_disc_cancel();                       /* must stop scanning before connect */
            ble_gap_connect(BLE_OWN_ADDR_PUBLIC, &ev->disc.addr, 30000, NULL, gap_cb, NULL);
        }
        return 0; }
    case BLE_GAP_EVENT_CONNECT:
        if (ev->connect.status == 0) peer_add(ev->connect.conn_handle),
            peer_disc_all(ev->connect.conn_handle, on_disc_complete, NULL);
        else scan();
        return 0;
    case BLE_GAP_EVENT_NOTIFY_RX:
        handle_notify(ev->notify_rx.attr_handle, ev->notify_rx.om);   /* om is an mbuf chain */
        return 0;
    case BLE_GAP_EVENT_DISCONNECT:
        peer_delete(ev->disconnect.conn.conn_handle); scan(); return 0;
    }
    return 0;
}
```

## Read, write, subscribe
```c
const struct peer_chr *c = peer_chr_find_uuid(peer, &MY_SVC_UUID.u, &MY_CHR_UUID.u);
ble_gattc_read(conn, c->chr.val_handle, on_read, NULL);
ble_gattc_write_flat(conn, c->chr.val_handle, buf, len, on_write, NULL);     /* with response */
ble_gattc_write_no_rsp_flat(conn, c->chr.val_handle, buf, len);              /* without */
const struct peer_dsc *cccd = peer_dsc_find_uuid(peer, &MY_SVC_UUID.u, &MY_CHR_UUID.u,
                                  BLE_UUID16_DECLARE(BLE_GATT_DSC_CLT_CFG_UUID16));
uint8_t on[2] = {1, 0};                                                       /* 2 = indicate */
ble_gattc_write_flat(conn, cccd->dsc.handle, on, 2, on_subscribed, NULL);
```
Copy data out of `om` with `ble_hs_mbuf_to_flat()`; long values arrive as chains.

## Rules
- Queue GATT requests and start the next one in the completion callback.
- Callbacks run in the NimBLE host task: never block there; post to your own queue.
- Cache handles per bonded peer if you want to skip discovery on reconnect.
- Set `CONFIG_BT_NIMBLE_MAX_CONNECTIONS` and `CONFIG_BT_NIMBLE_ROLE_CENTRAL=y`.

## Verify
- [ ] Reconnects automatically after the peripheral power-cycles.
- [ ] Notifications at the peripheral's max rate are processed without host task stalls.
- [ ] Connection handle cleanup on disconnect (no stale peer entries after 100 cycles).

## Checked
2026-10-26. ESP-IDF master (latest release v6.1, head 2026-10-23) and apache/mynewt-nimble master headers. Confirmed: ble_gap_disc and struct ble_gap_disc_params fields (passive, filter_duplicates, itvl, window), ble_gap_disc_cancel, ble_gap_connect arguments and the note that connecting is refused while scanning, BLE_GAP_EVENT_NOTIFY_RX, ble_gattc_write_flat, ble_gattc_write_no_rsp_flat, BLE_GATT_DSC_CLT_CFG_UUID16, ble_hs_adv_parse_fields, ble_hs_mbuf_to_flat; CONFIG_BT_NIMBLE_MAX_CONNECTIONS and CONFIG_BT_NIMBLE_ROLE_CENTRAL. Wrong: peer.c path (it lives under nimble/common/nimble_central_utils, not blecent). Removed unconfirmed procedure-concurrency and discovery-time claims.
Method: documentation only; no commands were run.
