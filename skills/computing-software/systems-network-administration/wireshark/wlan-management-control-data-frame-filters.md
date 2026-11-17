---
id: computing-software.systems-network-administration.wireshark.wlan-management-control-data-frame-filters
name: wlan-management-control-data-frame-filters
category: computing-software
field: systems-network-administration
product: wireshark
tags: [wireshark, wlan, wlan-frame-types, 802-11, management-frames, display-filters]
level: practitioner
status: verified
description: "Filter 802.11 management, control and data frames by type/subtype in Wireshark to follow association, authentication, block ack and power save behaviour."
sources:
  - https://www.wireshark.org/docs/dfref/w/wlan.html
  - https://wiki.wireshark.org/CaptureSetup/WLAN
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Management/control/data frame filters

`wlan.fc.type`: 0 management, 1 control, 2 data. `wlan.fc.type_subtype` combines both.

## Management (type 0)
```
wlan.fc.type_subtype == 0x0008      # beacon
wlan.fc.type_subtype == 0x0004      # probe request
wlan.fc.type_subtype == 0x0005      # probe response
wlan.fc.type_subtype == 0x000b      # authentication
wlan.fc.type_subtype == 0x0000      # association request; 0x0001 response
wlan.fc.type_subtype == 0x0002      # reassociation request (roaming)
wlan.fc.type_subtype == 0x000a      # disassociation
wlan.fc.type_subtype == 0x000c      # deauthentication
wlan.fc.type_subtype == 0x000d      # action (BSS transition, block ack setup, radio measurement)
```
## Control (type 1)
```
wlan.fc.type_subtype == 0x001b      # RTS
wlan.fc.type_subtype == 0x001c      # CTS
wlan.fc.type_subtype == 0x001d      # ACK
wlan.fc.type_subtype == 0x0019      # block ack
```
## Data (type 2)
```
wlan.fc.type_subtype == 0x0028      # QoS data
wlan.fc.type_subtype == 0x002c      # QoS null (power save signalling)
wlan.fc.pwrmgt == 1                 # client entering power save
eapol                               # 4-way handshake
```

## A client connection, in order
Probe req/resp, Authentication (open or SAE), Association req/resp (status 0 = success), EAPOL
1-4 (or 802.1X EAP first), DHCP. Narrow to one client: `wlan.addr == aa:bb:cc:dd:ee:ff`.

## Hide beacon noise
```
!(wlan.fc.type_subtype == 0x0008) && !(wlan.fc.type == 1)
```

## Gotchas
- ACK and CTS frames carry only a receiver address (no transmitter): `wlan.addr == <client>` matches the ones sent TO the client but not the ones the client sent, which have no address at all. RTS and block ack carry both.
- Encrypted data frames show only 802.11 headers unless decrypted (WPA2-PSK with passphrase + 4-way handshake).

## Verify
- [ ] The association status code is 0 and EAPOL 1-4 completes for the client under test.

## Checked
Run on Wireshark 4.4.1 with a scapy radiotap capture holding one frame of every subtype in the lists: each
`wlan.fc.type_subtype` value decoded to the stated name (beacon 0x0008, probe request 0x0004 and response 0x0005,
authentication 0x000b, association 0x0000 and 0x0001, reassociation request 0x0002, disassociation 0x000a, deauthentication
0x000c, action 0x000d, RTS 0x001b, CTS 0x001c, ACK 0x001d, block ack 0x0019, QoS data 0x0028, QoS null 0x002c), the type
numbers were 0, 1 and 2, `wlan.fc.pwrmgt == 1` matched the power-save QoS null, `eapol` the key frame, the beacon-hiding filter
dropped only beacons and control frames, and `wlan.ta` was empty on ACK and CTS. `wlan.fixed.status_code` exists. The connection
order is the standard 802.11 sequence; the encryption note is a limitation statement, not measured.
