---
id: computing-software.firmware-embedded-development.esp-idf.esp-now-peer-messaging
name: esp-now-peer-messaging
category: computing-software
field: firmware-embedded-development
product: esp-idf
tags: [esp-wifi, esp-now, connectionless, peer-list, pmk-lmk, broadcast, send-callback, channel-matching, esp-idf, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Use ESP-NOW for low-latency connectionless messaging between ESP32s: peer setup, encryption keys, channel matching with Wi-Fi, payload limits and delivery semantics."
sources:
  - https://github.com/espressif/esp-idf/blob/master/docs/en/api-reference/network/esp_now.rst
  - https://github.com/espressif/esp-idf/blob/master/components/esp_wifi/include/esp_now.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ESP-NOW peer messaging

**Goal:** fast, router-free messaging between ESP32 nodes, e.g. battery
sensors to a gateway, remotes to actuators.

## Basics
- Vendor-specific 802.11 action frames; no association needed.
- Payload up to **250 bytes** (`ESP_NOW_MAX_DATA_LEN`, v1.0); v2.0 devices allow up to 1470
  bytes (`ESP_NOW_MAX_DATA_LEN_V2`) and can receive from v1.0 devices, but v1.0 devices cannot
  receive the longer packets.
- Up to 20 peers in the peer list (`ESP_NOW_MAX_TOTAL_PEER_NUM`), of which at most 6 can be
  encrypted (`ESP_NOW_MAX_ENCRYPT_PEER_NUM`).

## Setup
```c
esp_netif_init(); esp_event_loop_create_default();
wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
esp_wifi_init(&cfg);
esp_wifi_set_storage(WIFI_STORAGE_RAM);
esp_wifi_set_mode(WIFI_MODE_STA);
esp_wifi_start();
esp_wifi_set_channel(1, WIFI_SECOND_CHAN_NONE);     /* all nodes on the same channel */

esp_now_init();
esp_now_register_send_cb(on_sent);                   /* keep callbacks short */
esp_now_register_recv_cb(on_recv);
esp_now_peer_info_t peer = { .channel = 1, .ifidx = WIFI_IF_STA, .encrypt = false };
memcpy(peer.peer_addr, gateway_mac, 6);
esp_now_add_peer(&peer);
esp_now_send(gateway_mac, buf, len);
```

## Delivery semantics
- The send callback reports `ESP_NOW_SEND_SUCCESS` if the data was received at the MAC layer,
  which does **not** mean your application processed it. Add an application-level
  ack/sequence number if it matters.
- Queue sends and let the callback report each result before sending the next.

## Channel matching (the common failure)
All nodes must be on the same channel. If the gateway is also a Wi-Fi STA connected to a
router, **its channel is the router's channel** and can change. Options: put sensors in a
channel scan loop (try channels until ACK), have the gateway broadcast its channel, or fix the
router's channel.

## Security
`esp_now_set_pmk()` (primary master key, 16 bytes; a default PMK is used if you do not set one)
plus a per-peer 16-byte `lmk` with `encrypt = true` encrypts unicast frames. Encrypting
multicast vendor-specific action frames is not supported. Keys hard-coded across a fleet
are weak; provision per-device keys.

## Power
A sensor can skip association and TCP: start Wi-Fi, initialise ESP-NOW, send, then sleep.
Measure the awake time on your hardware.

## Verify
- [ ] Send callback success rate > 99 % at intended range; app-level acks for critical data.
- [ ] Behaviour when the gateway's router changes channel is tested.

## Checked
2026-10-26. ESP-IDF master docs, latest release v6.1 (repository head 2026-10-23). Confirmed in esp_now.h and the ESP-NOW guide: 250-byte v1.0 and 1470-byte v2.0 limits, 20 total / 6 encrypted peers, 16-byte PMK/LMK and default PMK, send callback semantics (MAC-layer receipt), multicast frames cannot be encrypted, Wi-Fi must be started before esp_now_init. Wrong: "6-17 encrypted peers" (the constant is 6). Removed unconfirmed latency figures, the v2 "IDF 5.4+" gate, CCMP and broadcast ACK/retry claims.
Method: documentation only; no commands were run.
