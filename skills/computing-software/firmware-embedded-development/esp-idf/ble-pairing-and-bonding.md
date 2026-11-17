---
id: computing-software.firmware-embedded-development.esp-idf.ble-pairing-and-bonding
name: ble-pairing-and-bonding
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-ble, ble-pairing, le-secure-connections, passkey-entry, numeric-comparison, bonding-storage, io-capabilities, just-works, mitm-protection, esp-idf, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Configure BLE pairing and bonding on ESP32 NimBLE: IO capabilities, LE Secure Connections, passkey events, bond storage in NVS, and re-pairing when a phone forgets the device."
sources:
  - https://github.com/apache/mynewt-nimble/blob/master/nimble/host/include/host/ble_hs.h
  - https://github.com/apache/mynewt-nimble/blob/master/nimble/host/include/host/ble_gap.h
  - https://github.com/apache/mynewt-nimble/blob/master/nimble/host/include/host/ble_sm.h
  - https://github.com/espressif/esp-idf/blob/master/components/bt/host/nimble/Kconfig.in
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BLE pairing and bonding (ESP-IDF NimBLE)

**Goal:** encrypted, authenticated links where needed, without making setup painful or locking
users out after a phone reset.

## Association model follows IO capabilities
| Device IO | Phone (display + keyboard) | Model | MITM protection |
|---|---|---|---|
| NoInputNoOutput | any | Just Works | **no** |
| DisplayOnly | keyboard | Passkey entry (device shows 6 digits) | yes |
| KeyboardOnly | display | Passkey entry (user types on device) | yes |
| DisplayYesNo | display | Numeric comparison (LESC) | yes |
A headless device without display can still get MITM protection with a **static passkey printed
on the label** (weaker, but far better than Just Works), or out-of-band (NFC).

## NimBLE configuration
```c
ble_hs_cfg.sm_io_cap = BLE_SM_IO_CAP_DISP_ONLY;
ble_hs_cfg.sm_bonding = 1;
ble_hs_cfg.sm_mitm = 1;
ble_hs_cfg.sm_sc = 1;                         /* LE Secure Connections (ECDH) */
ble_hs_cfg.sm_our_key_dist = BLE_SM_PAIR_KEY_DIST_ENC | BLE_SM_PAIR_KEY_DIST_ID;
ble_hs_cfg.sm_their_key_dist = BLE_SM_PAIR_KEY_DIST_ENC | BLE_SM_PAIR_KEY_DIST_ID;
ble_hs_cfg.store_status_cb = ble_store_util_status_rr;   /* evict oldest bond when full */
ble_store_config_init();                     /* bond storage; persists in NVS with CONFIG_BT_NIMBLE_NVS_PERSIST=y */
```
Passkey event in the GAP handler:
```c
case BLE_GAP_EVENT_PASSKEY_ACTION:
    if (event->passkey.params.action == BLE_SM_IOACT_DISP) {
        struct ble_sm_io pk = { .action = BLE_SM_IOACT_DISP, .passkey = random_6_digits() };
        show_on_display(pk.passkey);
        ble_sm_inject_io(event->passkey.conn_handle, &pk);
    }
    break;
```
Require security on sensitive characteristics with `BLE_GATT_CHR_F_*_AUTHEN` flags so access
triggers pairing automatically.

## The "phone forgot the device" problem
If the phone deletes its bond but the device keeps its own, re-pairing fails (keys mismatch).
Handle `BLE_GAP_EVENT_REPEAT_PAIRING`: delete the old bond for that peer
(`ble_store_util_delete_peer`) and return `BLE_GAP_REPEAT_PAIRING_RETRY` (or `BLE_GAP_REPEAT_PAIRING_IGNORE`). With `CONFIG_BT_NIMBLE_HANDLE_REPEAT_PAIRING_DELETION=y` (default off) the stack deletes the bond itself and posts no event. Also provide a
user-visible "clear bonds" action (button hold) for support.

## Gotchas
- Legacy pairing (sm_sc = 0) with Just Works is trivially sniffable; use LESC.
- Bond table size `CONFIG_BT_NIMBLE_MAX_BONDS` (default 3): when full, the overflow policy (Kconfig choice: oldest bond or least recently used) decides what is removed; the `store_status_cb` handler must be set for eviction to happen.
- After firmware changes that alter the GATT table, have the phone forget the device and re-pair.

## Verify
- [ ] Sniffer (nRF Sniffer) shows encrypted traffic after pairing.
- [ ] Phone forgets device -> re-pair works without resetting the device.
- [ ] Protected characteristic unreadable before pairing.

## Checked

2026-10-25, against the ESP-IDF documentation source (espressif/esp-idf docs/en, master, v6.1 release period). Confirmed from the NimBLE headers and ESP-IDF NimBLE Kconfig: ble_hs_cfg sm_* fields and store_status_cb, BLE_SM_IO_CAP_* and BLE_SM_IOACT_* names, BLE_GAP_EVENT_PASSKEY_ACTION and REPEAT_PAIRING with RETRY/IGNORE return codes, ble_store_util_status_rr and ble_store_util_delete_peer, BT_NIMBLE_MAX_BONDS (default 3), NVS_PERSIST. Added the stack-side repeat-pairing option. Removed the unconfirmed iOS caching claim. The association-model table follows the Bluetooth Core specification and was not re-checked against it.
Method: documentation only; no commands were run.
