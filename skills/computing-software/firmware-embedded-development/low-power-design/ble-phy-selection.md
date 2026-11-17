---
id: computing-software.firmware-embedded-development.low-power-design.ble-phy-selection
name: ble-phy-selection
category: computing-software
field: firmware-embedded-development
product: low-power-design
tags: [ble-phy, le-2m, le-coded, phy-update, long-range-ble, airtime, low-power, firmware-embedded-development]
level: practitioner
status: draft
description: "Choose BLE PHYs for energy and range: 1M vs 2M vs Coded S2/S8 airtime, PHY update requests, extended advertising on Coded PHY, and measuring energy per byte."
sources:
  - https://www.bluetooth.com/blog/exploring-bluetooth-5-going-the-distance/
  - https://docs.zephyrproject.org/latest/connectivity/bluetooth/api/connection_mgmt.html
  - https://docs.nordicsemi.com/bundle/ncs-latest/page/nrf/protocols/bt/index.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# BLE PHY selection

## The PHYs
| PHY | Air rate | Range (relative) | Airtime for 251-byte PDU |
|---|---|---|---|
| LE 1M | 1 Mbit/s | 1x | ~2.1 ms |
| LE 2M | 2 Mbit/s | ~0.8x (about 3-5 dB less sensitivity) | ~1.06 ms |
| LE Coded S=2 | 500 kbit/s | ~2x | ~4.5 ms |
| LE Coded S=8 | 125 kbit/s | ~4x | ~17 ms |

Radio energy scales with airtime at roughly constant TX/RX current, so **2M halves energy per byte**
and lowers collision probability. Coded PHY buys range (link budget +12 dB at S=8) at 4-8x the
energy per byte.

## Selecting at runtime
Central or peripheral can request a PHY update after connection:
```c
/* Zephyr */
struct bt_conn_le_phy_param p = BT_CONN_LE_PHY_PARAM_2M;
bt_conn_le_phy_update(conn, &p);
/* callback le_phy_updated(conn, info) reports info->tx_phy / rx_phy */
```
nRF5 SDK: `sd_ble_gap_phy_update()`. ESP-IDF NimBLE: `ble_gap_set_prefered_le_phy()`. The peer may
refuse (phones support 2M widely, Coded less so: check iOS/Android model support).

## Advertising
- Legacy advertising is always 1M.
- Extended advertising can use Coded PHY for primary and secondary channels (long-range beacons)
  or 2M on the secondary channel to shorten large payloads. Scanners must support extended
  scanning on that PHY.

## Strategy
- Default to 2M for bulk transfers (OTA, logs) when RSSI is good (> about -75 dBm).
- Fall back to 1M, then Coded, as RSSI drops or packet error rate rises; switch back with
  hysteresis.
- Pair PHY with Data Length Extension (251-byte PDUs) and a suitable connection interval for best
  energy per byte.

## Gotchas
- Coded PHY increases connection event length; with short connection intervals the radio may be
  on most of the time.
- Some controllers need the feature enabled at build time (`CONFIG_BT_CTLR_PHY_CODED=y`,
  `CONFIG_BT_CTLR_PHY_2M=y`).

## Verify
- [ ] Energy per transferred kilobyte measured on 1M and 2M; 2M lower at good RSSI.
- [ ] PHY switching logic keeps the link alive when walking out of range.
