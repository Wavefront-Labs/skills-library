---
id: computing-software.firmware-embedded-development.low-power-design.ble-connection-interval-and-latency
name: ble-connection-interval-and-latency
category: computing-software
field: firmware-embedded-development
product: low-power-design
tags: [radio-power, ble-connection-interval, peripheral-latency, supervision-timeout, connection-parameter-update, ppcp, throughput-vs-power, firmware-embedded-development]
level: advanced
status: gated
description: "Tune BLE connection interval, peripheral latency and supervision timeout for power vs responsiveness, request updates from the peripheral, and handle phone limits."
sources:
  - https://www.bluetooth.com/specifications/specs/core-specification-6-0/
  - https://developer.apple.com/accessories/Accessory-Design-Guidelines.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BLE connection interval and peripheral latency

**Goal:** a connected peripheral that sleeps most of the time but still responds quickly
enough and never drops the connection unexpectedly.

## Parameters
- **Connection interval** (1.25 ms units; Core Specification range 7.5 ms to 4 s): how often central and peripheral meet.
- **Peripheral latency** (slave latency, Core Specification range 0-499): number of events the peripheral may skip when
  it has nothing to send. Effective peripheral wake period = interval x (latency + 1), while it
  can still respond within one interval when it does have data.
- **Supervision timeout** (Core Specification range 100 ms to 32 s): link declared lost after this much silence. Must be
  > (1 + latency) x interval x 2.
  (gated: unconfirmed, source is paywalled or blocked)

## Power
Average current is roughly the energy of one connection event divided by the effective period; measure it on
your radio. Use latency instead of a long
interval when you need fast host-to-device responses only occasionally: interval 30 ms with
latency 30 gives ~1 s idle wake period but sends device-initiated data within 30 ms.
Note that host-to-device writes may wait up to (latency + 1) intervals if the peripheral is
skipping events.

## Who decides
The **central** (phone) sets the parameters. The peripheral requests changes:
- GAP Peripheral Preferred Connection Parameters characteristic (read by some centrals; Apple's guidelines say
  iOS does not read it).
- L2CAP Connection Parameter Update Request / LL Connection Parameters Request after
  connecting (your host stack's connection-parameter-update call).
Wait a few seconds after connection (service discovery is faster at short intervals), then
request the low-power set. Request short intervals again during bulk transfer (DFU).

## Phone constraints
- Apple's Accessory Design Guidelines (Bluetooth Low Energy, Connection Parameters) say a request may be
  rejected unless: latency <= 30, supervision timeout 6 to 18 s, interval min >= 15 ms and <= 2 s and a multiple
  of 15 ms, interval max at least 15 ms above interval min (or both 15 ms), interval max x (latency + 1) <= 6 s,
  and timeout > interval max x (latency + 1) x 3. Apple Watch wants multiples of 30 ms. Use the procedure
  the accessory supports (Connection Parameters Request) rather than the preferred-parameters characteristic.
- Android behaviour differs by version; test on real phones.
- Always read back the actual parameters in the `le_param_updated` callback; don't assume.

## Verify
- [ ] Idle connected current measured with real iOS and Android phones.
- [ ] Response latency for device notifications and phone writes measured at the chosen set.
- [ ] No supervision timeouts over a 24 h connection soak.

## Checked
2026-11-01. Confirmed in Apple's Accessory Design Guidelines (Bluetooth Low Energy, Connection Parameters): the
iOS request rules above, the Connection Parameters Request procedure, and that the preferred-parameters
characteristic is not read. These replace the older, different numbers. Removed: nRF52 current figures, Zephyr and
NimBLE function and Kconfig names, Android default intervals. Gated: the Core Specification ranges for
interval, latency and supervision timeout, because the Bluetooth specification page could not be read.
Method: documentation only; no commands were run.
