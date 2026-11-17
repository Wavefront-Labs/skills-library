---
id: computing-software.systems-network-administration.zigbee2mqtt.zigbee2mqtt-network-key-channel-panid
name: zigbee2mqtt-network-key-channel-panid
category: computing-software
field: systems-network-administration
product: zigbee2mqtt
tags: [zigbee2mqtt, network-key, pan-id, ext-pan-id, channel, zll, wifi-interference, re-pairing, secret]
level: advanced
status: docs-checked
description: "Manage Zigbee2MQTT network_key, pan_id and channel: GENERATE values, secret.yaml storage, live channel change on zstack and ember, and which changes force re-pairing."
sources: ["https://www.zigbee2mqtt.io/guide/configuration/zigbee-network.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Zigbee2MQTT network key, PAN ID and channel

```yaml
advanced:
    pan_id: 0x1a62            # GENERATE for a new random one
    ext_pan_id: [0xDD, 0xDD, 0xDD, 0xDD, 0xDD, 0xDD, 0xDD, 0xDD]
    channel: 11               # default 11; ZLL channels 11, 15, 20, 25 avoid problems
    network_key: GENERATE
```

- `network_key: GENERATE` makes Zigbee2MQTT create a random 128-bit key at next start and write it into `configuration.yaml`. Changing the key requires re-pairing every device. The old default key `[1, 3, 5, 7, 9, 11, 13, 15, 0, 2, 4, 6, 8, 10, 12, 13]` is public, so replace it on any network still using it (the security page says so strongly).
- PAN ID and extended PAN ID are identifiers, not security; changing them also means re-pairing and is mainly for resolving a clash with a nearby network.
- Store the key outside the main file: `network_key: '!secret.yaml network_key'` (quotes required) and put the list in `secret.yaml`.

Changing channel on an existing network is supported only for the `zstack` and `ember` adapters. Zigbee2MQTT broadcasts a network update at startup when the configured channel differs from the adapter's:

```
warning: zh:controller: Configured channel '18' does not match adapter channel '19', changing channel
warning: zh:controller: Channel changed to '19'
```

Sleeping battery devices switch only when they next wake, so trigger them (press a button) after the change. Some devices do not support channel changes; if one stays unresponsive for several minutes after being woken, re-pair it manually.

Choosing a channel: Wi-Fi and Zigbee share 2.4 GHz, so pick a Zigbee channel away from your Wi-Fi channels.

## Checked

2026-11-03. Confirmed against the Zigbee network page and the Securing page: pan_id, ext_pan_id, channel default and ZLL channels, GENERATE, re-pairing, old default key, secret.yaml syntax, channel change support for zstack and ember, log lines, sleeping device and unsupported device warnings, Wi-Fi interference. Nothing removed.
Method: documentation only; no commands were run.
