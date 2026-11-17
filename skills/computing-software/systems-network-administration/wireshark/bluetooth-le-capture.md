---
id: computing-software.systems-network-administration.wireshark.bluetooth-le-capture
name: bluetooth-le-capture
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, bluetooth-le, ble, btle, nrf-sniffer, hci-capture]
level: practitioner
status: draft
description: "Capture Bluetooth LE with an nRF sniffer extcap, Android HCI snoop logs or Linux btmon, and analyse advertising, connections, GATT and pairing."
sources:
  - https://wiki.wireshark.org/Bluetooth
  - https://www.nordicsemi.com/Products/Development-tools/nRF-Sniffer-for-Bluetooth-LE
  - https://source.android.com/docs/core/connect/bluetooth/verifying_debugging
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bluetooth LE capture

## Capture options
| Method | Sees |
|--------|------|
| Nordic nRF Sniffer (nRF52840 dongle + extcap plugin) | over-the-air advertising and one followed connection |
| Android "Bluetooth HCI snoop log" (developer options) | host-controller traffic of that phone, `btsnoop_hci.log` via bugreport |
| Linux `btmon -w trace.btsnoop` or Wireshark `bluetooth0` interface | HCI of the local adapter |
| iOS PacketLogger (Xcode additional tools) with Bluetooth logging profile | HCI of the iPhone |

HCI captures see only what the local host sends/receives, but decrypted. Air sniffers see any device
but need the pairing (LTK) to decrypt encrypted links.

## Filters
```
btle.advertising_header.pdu_type == 0x00     # ADV_IND
btcommon.eir_ad.entry.device_name
btle.advertising_address == aa:bb:cc:dd:ee:ff
btatt                                         # GATT reads/writes/notifications
btatt.opcode == 0x52                          # Write Command
btsmp                                         # pairing
```

## Following a connection (nRF Sniffer)
Select the device in the extcap toolbar's device list so the sniffer follows CONNECT_IND and channel
hopping. Start before the connection is made.

## Pairing and encryption
LE Legacy pairing with Just Works/passkey can be cracked offline (crackle) from a captured pairing;
LE Secure Connections cannot. Provide the LTK in Bluetooth preferences to decrypt.

## Verify
- [ ] The target's advertisements appear and, after connecting, ATT read/write operations decode.
